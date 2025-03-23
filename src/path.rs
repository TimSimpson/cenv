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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_path_seperator() {
        assert_eq!(_get_path_seperator(false), ';');
        assert_eq!(_get_path_seperator(true), ':');
    }
}
