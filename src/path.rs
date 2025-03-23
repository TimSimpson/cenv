pub fn get_path_seperator() -> char {
    _get_path_seperator(cfg!(windows))
}

fn _get_path_seperator(not_windows: bool) -> char {
    if not_windows {
        ':'
    } else {
        ';'
    }
}

pub struct PathUpdater {
    path_seperator: char,
    case_sensitive: bool,
}

pub struct UpdatePathArgs<'a> {
    new_path: &'a Vec<&'a str>,
    old_path: &'a Vec<&'a str>,
}

impl PathUpdater {
    pub fn new(path_seperator: char) -> Self {
        Self {
            path_seperator,
            case_sensitive: cfg!(windows),
        }
    }

    pub fn new2(path_seperator: char, case_sensitive: bool) -> Self {
        Self {
            path_seperator,
            case_sensitive,
        }
    }

    fn _normalize_path_value(&self, path: &str) -> String {
        if self.case_sensitive {
            path.to_string()
        } else {
            path.to_lowercase()
        }
    }

    fn _normalize_path_arg(&self, path_arg: &Vec<&str>) -> Vec<String> {
        path_arg
            .iter()
            .map(|p| self._normalize_path_value(p))
            .collect()
    }

    fn _remove_matching_elements<'a>(
        &self,
        new_path: &'a Vec<&str>,
        old_path: &'a Vec<&str>,
    ) -> (Vec<&'a str>, Vec<String>) {
        let mut norm_old_path = self._normalize_path_arg(old_path);
        let mut new_path_list = new_path.clone();
        let mut norm_new_path = self._normalize_path_arg(new_path);

        for i in 0..norm_old_path.len() {
            while i < norm_old_path.len() && norm_new_path.contains(&norm_old_path[i]) {
                loop {
                    let delete_index = norm_new_path.iter().position(|p| p == &norm_old_path[i]);
                    match delete_index {
                        None => break,
                        Some(delete_index) => {
                            norm_new_path.remove(delete_index);
                            new_path_list.remove(delete_index);
                        }
                    }
                }
                norm_old_path.remove(i);
            }
        }
        (new_path_list, norm_old_path)
    }

    /// Given the name of an environment variables, retrieves it's value and
    /// determines what the list of paths it's referencing are. Then removes any
    /// paths found in "old_path" (only removes them once for each time they
    /// appear). Will also add paths from "new_path".
    pub fn update_paths<'a>(
        &self,
        path_var_name: &str,
        new_path: &'a Vec<&'a str>,
        old_path: &'a Vec<&'a str>,
    ) -> String {
        let (new_path, old_path) = self._remove_matching_elements(new_path, old_path);

        let original_value = std::env::var(path_var_name).unwrap_or_default();
        let original_list = original_value
            .split(self.path_seperator)
            .collect::<Vec<&str>>();

        let modified_list = self._update_paths(&original_list, &new_path, &old_path);

        let modified_value = modified_list.join(&self.path_seperator.to_string());
        modified_value
    }

    pub fn _update_paths<'a>(
        &self,
        original_list: &Vec<&'a str>,
        new_path: &Vec<&'a str>,
        old_path: &Vec<String>,
    ) -> Vec<&'a str> {
        let lc_list = original_list
            .iter()
            .map(|p| self._normalize_path_value(p))
            .collect::<Vec<String>>();

        let mut remove_indices = Vec::new();

        for op in old_path {
            match lc_list.iter().position(|p| p == op) {
                None => continue,
                Some(index) => {
                    remove_indices.push(index);
                }
            }
        }

        let filtered_list: Vec<&str> = original_list
            .iter()
            .enumerate()
            .filter(|(i, _)| !remove_indices.contains(&i))
            .map(|(_, p)| *p)
            .collect();

        let mut modified_list = new_path.clone();
        modified_list.extend(filtered_list);

        modified_list
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_path_seperator() {
        assert_eq!(_get_path_seperator(false), ';');
        assert_eq!(_get_path_seperator(true), ':');
    }


    #[test]
    fn test_update_paths_test_empty() {
        let pu = PathUpdater::new2('?', true);
        let expected = Vec::<&str>::new();
        let original_list: Vec<&str> = Vec::new();
        let new_path: Vec<&str> = Vec::new();
        let old_path: Vec<String> = Vec::new();
        let actual = pu._update_paths(&original_list, &new_path, &old_path);
        assert_eq!(expected, actual)
    }
}
