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
    get_env_var: fn(&str)->String,
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
            get_env_var: |n| std::env::var(n).unwrap_or_default(),
        }
    }

    pub fn new2(path_seperator: char, case_sensitive: bool) -> Self {
        Self {
            path_seperator,
            case_sensitive,
            get_env_var: |n| std::env::var(n).unwrap_or_default(),
        }
    }

    pub fn new3(path_seperator: char, case_sensitive: bool, get_env_var: fn(&str)->String) -> Self {
        Self {
            path_seperator,
            case_sensitive,
            get_env_var,
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

        let original_value = (self.get_env_var)(path_var_name);
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
        let actual = pu._update_paths(&Vec::new(), &Vec::new(), &Vec::new());
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_update_paths_test_remove_one() {
        let pu = PathUpdater::new2('?', true);
        let expected = Vec::<&str>::new();
        let actual = pu._update_paths(&vec!["abc"], &Vec::new(), &vec!["abc".to_string()]);
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_update_paths_test_remove_only_takes_one() {
        let pu = PathUpdater::new2('?', true);
        // Makes certain we only remove one instance. This is for cases where
        // a user may have activated an environment and caused locations to be
        // added to their path which were already in the path, and we don't
        // want to purge everything.
        let expected = vec!["abc", "abc"];
        let actual = pu._update_paths(&vec!["abc", "abc", "abc"], &Vec::new(), &vec!["abc".to_string()]);
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_update_paths_test_remove_when_case_sensitive() {
        let pu = PathUpdater::new2('?', true);
        let expected = vec!["aBC", "Abc"];
        let actual = pu._update_paths(&vec!["aBC", "Abc", "abc"], &Vec::new(), &vec!["abc".to_string()]);
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_update_paths_test_remove_when_case_insensitive() {
        let pu = PathUpdater::new2('?', false);
        let expected = vec!["Abc", "abc"];
        let actual = pu._update_paths(&vec!["aBC", "Abc", "abc"], &Vec::new(), &vec!["abc".to_string()]);
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_update_paths_test_add_one() {
        let pu = PathUpdater::new2('?', true);
        let expected = vec!["aBc"];
        let actual = pu._update_paths(&Vec::new(), &vec!["aBc"], &Vec::new());
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_update_paths_test_add_one_case_insensitive() {
        let pu = PathUpdater::new2('?', false);
        // Ensure that even on case insensitive platforms the exact string
        let expected = vec!["aBc"];
        let actual = pu._update_paths(&Vec::new(), &vec!["aBc"], &Vec::new());
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_update_paths_test_add_one_multiples_case_insensitive() {
        let pu = PathUpdater::new2('?', false);
        // Ensure that even on case insensitive platforms the exact string
        let expected = vec!["aBc", "aBC", "abc"];
        let actual = pu._update_paths(&vec!["abc"], &vec!["aBc", "aBC"], &Vec::new());
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_update_paths_test_add_and_remove() {
        let pu = PathUpdater::new2('?', false);
        // Ensure that even on case insensitive platforms the exact string
        let expected = vec!["fgh", "abc"];
        let actual = pu._update_paths(&vec!["abc", "cde"], &vec!["fgh"], &vec!["cde".to_string()]);
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_update_paths_test_add_and_remove_2() {
        let pu = PathUpdater::new2('?', false);
        // Ensure that even on case insensitive platforms the exact string
        let expected = vec!["fgh", "123", "abc"];
        let actual = pu._update_paths(&vec!["abc", "cde"], &vec!["fgh", "123"], &vec!["cde".to_string()]);
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_interface_test_does_nothing() {
        let pu = PathUpdater::new3(':', true, |_| "".to_string());
        let expected = "".to_string();
        let actual = pu.update_paths("PATH", &Vec::new(), &Vec::new());
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_interface_test_removes_one() {
        let pu = PathUpdater::new3(':', true, |_| "abc:def".to_string());
        let expected = "abc".to_string();
        let actual = pu.update_paths("PATH", &Vec::new(), &vec!["def"]);
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_interface_test_removes_two() {
        let pu = PathUpdater::new3(':', true, |_| "abc:def:ghi".to_string());
        let expected = "def".to_string();
        let actual = pu.update_paths("PATH", &Vec::new(), &vec!["ghi", "abc"]);
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_interface_test_removes_only_one() {
        let pu = PathUpdater::new3(';', false, |_| "AbC;abc;def".to_string());
        let expected = "abc;def".to_string();
        let actual = pu.update_paths("PATH", &Vec::new(), &vec!["abc"]);
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_interface_test_removes_only_one_case_sensitive() {
        let pu = PathUpdater::new3(':', true, |_| "AbC:abc:def".to_string());
        let expected = "AbC:def".to_string();
        let actual = pu.update_paths("PATH", &Vec::new(), &vec!["abc"]);
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_interface_test_adds_one() {
        let pu = PathUpdater::new3(':', true, |_| "abc:def".to_string());
        let expected = "123:abc:def".to_string();
        let actual = pu.update_paths("PATH", &vec!["123"], &Vec::new());
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_interface_test_adds_two() {
        let pu = PathUpdater::new3(':', true, |_| "abc:def".to_string());
        let expected = "123:abc:abc:def".to_string();
        let actual = pu.update_paths("PATH", &vec!["123", "abc"], &Vec::new());
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_interface_test_removes_matching_paths() {
        let pu = PathUpdater::new3(':', true, |_| "abc:def".to_string());
        let expected = "abc:def".to_string();
        let actual = pu.update_paths("PATH", &vec!["1", "2"], &vec!["1", "2"]);
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_interface_test_removes_matching_paths_2() {
        let pu = PathUpdater::new3(':', true, |_| "123:456".to_string());
        let expected = "abC:DeFh:123:456".to_string();
        // Note that abC and ABc are treated differently, because it's case
        // sensitive.
        let actual = pu.update_paths("PATH", &vec!["abC", "DeFh"], &vec!["ABc", "dEf"]);
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_interface_test_removes_matching_paths_3() {
        let pu = PathUpdater::new3(';', false, |_| "123;456".to_string());
        let expected = "DeFh;123;456".to_string();
        // Unlike above, 'abC' == 'ABc' because it's case insensitive.
        let actual = pu.update_paths("PATH", &vec!["abC", "DeFh"], &vec!["ABc", "dEf"]);
        assert_eq!(expected, actual)
    }
}
