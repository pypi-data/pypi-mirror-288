use rustypath::RPath;
use colorized::*;
use pyo3::prelude::*;

pub struct File {
    path: RPath,
    duplicates: Vec<RPath>,
}

pub struct Files {
    files: Vec<File>,
}

struct Count {
    value: u64,
}

impl Count {
    fn get(&self) -> u64 {
        self.value
    }

    fn add(&mut self, val: u64) {
        self.value = self.value + val;
    }

    fn new() -> Self{
        Self{
            value:0,
        }
    }
}

impl Files {
    pub fn new(path: RPath, recursive: bool, ignore: Vec<String>) -> Self {
        // println!("{:?}", ignore);
        if recursive {
            println!("-- {}","[Generating Directory Map]".color(Colors::YellowFg));
            let f = scan_recursive(&path, ignore);
            println!("-- {}","[Generated Directory Map]\n".color(Colors::GreenFg));
            Self {
                files: f,
            }
        } else {
            println!("-- {}","[Generating Directory Map]".color(Colors::YellowFg));
            let f = scan(&path);
            println!("-- {}","[Generated Directory Map]\n".color(Colors::GreenFg));
            Self{
                files: f,
            }
        }
    }

    pub fn find_duplicates(&mut self, explicit: bool) {
        // PRINCIPLE
        // only files that were scanned and that were found as a duplicate will be added to done list.
        // if a file is not scanned and not found as a duplicate, it will be subject to either of those things
        // therefore they will be scanned as a primary file or they will be found as a duplicate
        
        // MECHANISM
        // [FILES], [DONE]
        // -> take one file from [FILES] and scan it, also add it to [DONE]
        // -> take another file from [FILES] that is neither the same file as the previous file
        //    nor is added to [DONE]. Then scan it and if duplicate, then add it to the original file's duplicate list
        //    and push this current file to [DONE]
        // -> repeat for files not in [DONE]
        
        let mut done: Vec<String> = Vec::new(); // if a file is scanned, dont scan it again
        let mut count = Count::new();
        let start_time = std::time::Instant::now();
        for i in 0..=self.files.len()-1 {
            if !done.contains(&self.files[i].path.convert_to_string()) {
                if explicit {
                    println!("Scanning {}", self.files[i].path.convert_to_string().replace("\\\\?\\", ""));
                }
                // read each file's content and check with all other files except itself.
                let content = std::fs::read(self.files[i].path.convert_to_pathbuf().clone())
                    .expect(&("Unable to read ".to_string()+&self.files[i].path.convert_to_string()));

                let filesize = std::fs::metadata(self.files[i].path.convert_to_pathbuf()).expect(&("Failed to find file size.".to_string() + " " + &self.files[i].path.convert_to_string())).len();

                done.push(self.files[i].path.clone().convert_to_string());
                count.add(1);

                // let mut title_count = 0;
                // let mut filecounts = 1;

                for j in 0..=self.files.len()-1 {
                    if j == i {
                        continue;
                    } else if !done.contains(&self.files[j].path.convert_to_string()){
                        // if filesize of the comparing file is not filesize-200< size < filesize+200, dont compare
                        // this is a game changer -> super fast scanning.
                        // println!("{}", self.files[j].path.convert_to_string());
                        if filesize > 200{
                            if !(std::fs::metadata(self.files[j].path.convert_to_pathbuf()).expect(&("Failed to find file size.".to_string() + " " + &self.files[j].path.convert_to_string())).len() > filesize-200 && std::fs::metadata(self.files[j].path.convert_to_pathbuf()).expect(&("Failed to find file size.".to_string() + " " + &self.files[j].path.convert_to_string())).len() < filesize + 200) {
                                continue;
                            }
                        } else if filesize > 100 {
                            if !(std::fs::metadata(self.files[j].path.convert_to_pathbuf()).expect(&("Failed to find file size.".to_string() + " " + &self.files[j].path.convert_to_string())).len() > filesize-100 && std::fs::metadata(self.files[j].path.convert_to_pathbuf()).expect(&("Failed to find file size.".to_string() + " " + &self.files[j].path.convert_to_string())).len() < filesize + 100) {
                                continue;
                            }
                        } else if filesize < 100 {
                            if !(std::fs::metadata(self.files[j].path.convert_to_pathbuf()).expect(&("Failed to find file size.".to_string() + " " + &self.files[j].path.convert_to_string())).len() > 0 && std::fs::metadata(self.files[j].path.convert_to_pathbuf()).expect(&("Failed to find file size.".to_string() + " " + &self.files[j].path.convert_to_string())).len() < filesize+20) {
                                continue;
                            }
                        }
                        // read content
                        let content2 = std::fs::read(self.files[j].path.convert_to_pathbuf())
                            .expect(&("Unable to read ".to_string()+&self.files[j].path.convert_to_string()));

                        
                        if content == content2 {
                            let f = self.files[j].path.clone();
                            done.push(f.convert_to_string());
                            count.add(1);

                            self.files[i].duplicates.push(f);
                        }
                    } else {
                        // if already found as a duplicate of some file, nevermind.
                        continue;
                    }
                }
            }
        }

        let end_time = std::time::Instant::now();
        let runtime = end_time.duration_since(start_time);
        println!("");
        if runtime.as_secs_f64() >= 60.0 {
            println!("{} {} files in {:.2}m.", "Scanned".color(Colors::BlueFg), count.get(), runtime.as_secs_f64()/60.0);
        } else {
            println!("{} {} files in {:.3}s.", "Scanned".color(Colors::BlueFg), count.get(), runtime.as_secs_f64());
        }
    }

    pub fn show(&self) {
        for file in &self.files {
            if file.duplicates.len() > 0 {
                let mut string = file.path.convert_to_string().replace("\\\\?\\", "") + " -> {";

                let mut count = 0;

                for d in &file.duplicates {
                    if count > 0 {
                        string = string + ", " + &d.convert_to_string().replace("\\\\?\\", "").color(Colors::WhiteBg).color(Colors::RedFg);
                    } else {
                        string = string + " " + &d.convert_to_string().replace("\\\\?\\", "").color(Colors::WhiteBg).color(Colors::RedFg);
                    }
                    count += 1;
                }

                string = string + " }";

                if string != file.path.convert_to_string().replace("\\\\?\\", "") + " ->{ }" {
                    println!("{}", string);
                }
            }
        }
    }

    pub fn formatted(&self) {
        for file in &self.files {
            if file.duplicates.len() > 0 {
                println!("# {}", file.path.convert_to_string().replace("\\\\?\\", ""));

                for d in &file.duplicates {
                    println!("   {}  <- duplicate", d.convert_to_string().replace("\\\\?\\", "").color(Colors::WhiteBg).color(Colors::RedFg));
                }

                println!("");
            }
        }
    }

    pub fn delete_duplicates(&self, formatted: bool) {
        for file in &self.files {
            if file.duplicates.len() > 0 {
                if formatted {
                    println!("\n[DELETE]");
                    println!("{}", file.path.convert_to_string());
                } else {
                    println!("\n");
                }
                for d in &file.duplicates {
                    // delete
                    match std::fs::remove_file(d.convert_to_string()) {
                        Ok(_) => {
                            if formatted {
                                println!("   {} {}", "DELETE".color(Colors::RedFg), d.convert_to_string().replace("\\\\?\\", ""));
                            } else {
                                println!("{} {}", "DELETE".color(Colors::RedFg),  d.convert_to_string().replace("\\\\?\\", ""));
                            }
                        },
                        Err(e) => {
                            if formatted {
                                eprintln!("   {} {}: {}", "DELETE ERROR".color(Colors::RedFg), e, d.convert_to_string().replace("\\\\?\\", ""));
                            } else {
                                eprintln!("{} {}: {}", "DELETE ERROR".color(Colors::RedFg), e, d.convert_to_string().replace("\\\\?\\", ""));
                            }
                        }
                    }
                }
            }
        }
    }
}

fn scan_recursive(path: &RPath, ign: Vec<String>) -> Vec<File> {
    let mut ignore: Vec<String> = Vec::new();
    for x in &ign{
        ignore.push(x.clone().to_lowercase());
    }
    let mut file_rpaths: Vec<File> = Vec::new();

    if let Ok(entries) = std::fs::read_dir(path.convert_to_pathbuf()) {
        for entry in entries.flatten() {
            let file_path = entry.path();
            // println!("--hehe");
            if file_path.file_name().unwrap().to_str().unwrap().starts_with(".") {
                // println!("huhu");
                continue;
            }
            if file_path.is_dir() {
                if !ignore.contains(&file_path.file_name().unwrap().to_str().unwrap().to_lowercase()) {
                    // If the entry is a directory, recursively call scan on it
                    let subdirectory_files = scan_recursive(&RPath::new_from_pbuf(&file_path), ignore.clone());
                    for sub_file in subdirectory_files {
                        file_rpaths.push(sub_file);
                    }

                } else {
                    println!("skipping {:?}", &file_path);
                }
            } else {
                // If the entry is a file, add it to the list of files
                if let Some(file_name) = entry.file_name().to_str() {
                    // println!("Found {}", path.join(&file_name).convert_to_string());
                    file_rpaths.push(File {
                        path: path.join(&file_name),
                        duplicates: Vec::new(),
                    });
                }
            }
        }
    }

    file_rpaths
}

fn scan(path: &RPath) -> Vec<File> {
    let mut file_rpaths: Vec<File> = Vec::new();

    if let Ok(entries) = std::fs::read_dir(path.convert_to_pathbuf()) {
        for entry in entries.filter_map(Result::ok) {
            // let file_path = entry.path();
            // if file_path.file_name().unwrap().to_str().unwrap().starts_with(".") {
            //     // println!("huhu");
            //     continue;
            // }
            let metadata = entry.metadata().ok();
            if let Some(metadata) = metadata {
                if metadata.is_file() {
                    if let Some(_file_name) = entry.file_name().to_str() {
                        let file_path = entry.path();
                        file_rpaths.push(File {
                            path: RPath::new_from_pbuf(&file_path),
                            duplicates: Vec::new(),
                        });
                    }
                }
            }
        }
    }

    file_rpaths
}

// ---------------------------------------------

#[pyclass]
pub struct DetecteffRust {
    file_type: Files,
    formatted: bool,
}

#[pymethods]
impl DetecteffRust {
    #[new]
    pub fn new(path: &str, recursive: bool, formatted: bool, ignore: Vec<String>) -> PyResult<Self> {
        Ok(DetecteffRust{
            file_type: Files::new(RPath::new_from(path), recursive, ignore),
            formatted,
        })
    }

    pub fn find_duplicates(&mut self, explicit: bool) -> PyResult<()> {
        self.file_type.find_duplicates(explicit);
        println!("");

        if self.formatted {
            self.file_type.formatted();
        } else {
            self.file_type.show();
        }

        Ok(())
    }

    pub fn delete_duplicates(&mut self, found_already: bool, explicit: bool) -> PyResult<()> {
        
        if ! found_already {
            self.find_duplicates(explicit)?;
        }

        self.file_type.delete_duplicates(self.formatted);

        Ok(())
    }
}

#[pyfunction]
pub fn print_version() -> PyResult<()> {
    println!("detecteff {}", "v0.1".color(Colors::RedFg));
    std::process::exit(0);
}

#[pyfunction]
pub fn print_help() -> PyResult<()> {
    println!("detecteff {}", "help".color(Colors::YellowFg));
    println!("   -\n   {}","[INFO]".color(Colors::BlueFg));
    println!("   | -h, --help : show help text and exit.");
    println!("   | -v, --version : show version and exit.");
    println!("   -\n   {}","[FLAG]".color(Colors::BlueFg));
    println!("   | -r, --recursive : recursive mode. Default -> OFF");
    println!("   | -fmt, --formatted : show formatted output. Default -> OFF");
    println!("   -\n   {}","[INPUT]".color(Colors::BlueFg));
    println!("   | -s, --scan <directory> : scan the directory for duplicate files. ({})", "Mandatory".color(Colors::RedFg));
    println!("   | -i, --ignore <directory1>, <directory2>, ... : ignore these directories. ({})", "Optional".color(Colors::RedFg));
    println!("   -\n   {}", "[IRREVERSIBLE FLAG]".color(Colors::RedFg));
    println!("   | -del, --delete : delete any found duplicates. Default -> OFF");
    std::process::exit(0);
}

#[pymodule]
pub fn detecteff(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<DetecteffRust>()?;
    m.add_function(wrap_pyfunction!(print_help, m)?)?;
    m.add_function(wrap_pyfunction!(print_version, m)?)?;
    Ok(())
}