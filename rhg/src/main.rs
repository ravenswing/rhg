use dirs::home_dir;
use serde::Deserialize;
use std::fs::{File, read_to_string};
use std::io::{BufRead, BufReader, Error, Write};
use std::path::{Path, PathBuf};
use toml;

#[derive(Deserialize)]
pub struct Config {
    vault: String,
    steam_id: String,
}

#[derive(Debug, Clone)]
pub struct Note {
    pub path: PathBuf,
    pub name: String,
    pub content: Vec<String>,
}

impl Note {
    pub fn load(path: PathBuf) -> Result<Self, Error> {
        assert!(&path.exists(), "Unable to load note: {}", &path.display());

        let name = path.file_stem().unwrap().to_str().unwrap().to_string();

        // let input = File::open(&path)?;
        // let buffered = BufReader::new(input);
        // let content: () = buffered.lines();

        let content = read_to_string(&path)
            .unwrap() // panic on possible file-reading errors
            .lines() // split the string into an iterator of string slices
            .map(String::from) // make each slice into a string
            .collect(); // gather them together into a vector

        Ok(Self {
            path,
            name,
            content,
        })
    }

    pub fn new(path: PathBuf, name: String, content: Vec<String>) -> Self {
        Self {
            path,
            name,
            content,
        }
    }
}

fn main() {
    let home: String = home_dir()
        .expect("Failed to retrieve home directory.")
        .display()
        .to_string();

    let config_path = home + "/.config/rhg.toml";

    let toml_str = read_to_string(config_path).expect("Failed to read Cargo.toml file");
    let config: Config = toml::from_str(&toml_str).expect("Failed to deserialize Cargo.toml");

    let vault = Path::new(&config.vault);

    dbg!(&config.vault);

    // let note = Note { path, name };
    let note = Note {
        path: PathBuf::from("./test.md"),
        name: String::from("TEST"),
        content: vec![String::from("new line")],
    };

    println!("{:?}", note.name);

    // let path: &Path = Path::new(&note.path);
    //
    let second = Note::load(vault.join("test test.md")).unwrap();

    dbg!(&config.vault);
    dbg!(&second.content);
}
