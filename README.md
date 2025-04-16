# TaskManager
A Task manager for CS2450

### Authors:
- Matt Gubler
- Kevin Pett
- Michael Short
- Aidan Dougherty
----------------------------------------------------------
# Installation

## Download and Setup (All Operating Systems)

1. **Download the binary**
   - Visit the [releases page](#) to download the latest binary for your operating system

2. **Place the binary in your desired location**
   - Create a folder for the application (if it doesn't exist already):
      - This is where you will place the application and where it will create its json files

   - Make the binary executable (macOS/Linux only):
   ```
   chmod +x ~/PATH_TO_THE_PROGRAM
   ```
   for example:
   ```
   chmod +x ~/home/user/Documents/taskmanger/linux_taskmanager
   ```
3. **trust the developers of the file**
   - this will vary from system to system, but you may need to add addtional trust to the file to run it.

## Setting up API KEY

generate an api key at https://aistudio.google.com/app/apikey

### macOS

1. Open your shell profile file:
   ```
   # For bash users
   nano ~/.bash_profile
   
   # For zsh users (default in newer macOS)
   nano ~/.zshrc
   ```

2. Add the following line:
   ```
   export GEMINI_API_KEY=[your api key]
   ```
   *Do not include brackets [] in the key*

3. Save and close the file

4. Apply the changes:
   ```
   # For bash users
   source ~/.bash_profile
   
   # For zsh users
   source ~/.zshrc
   ```

### Windows

1. press windows and type 'cmd'
2. right click on the command line app and press run as administrator
3. enter the command:
   
   ```
   setx GEMINI_API_KEY "[your api key]"
   ```
   
   *Do not include brackets [] in the key*
5. press enter and exit

### Linux

1. Open your shell profile file:
   ```
   # For bash users
   nano ~/.bashrc
   
   # For other shells, use the appropriate config file
   ```

2. Add the following line:
   ```
   export GEMINI_API_KEY=[your api key]
   ```
   *Do not include brackets [] in the key*

3. Save and close the file

4. Apply the changes:
   ```
   source ~/.bashrc
   ```
Now just run the exicutible inside your folder to manage json task lists
## Repository Link:
https://github.com/MikeShort11/TaskManager

## Workflow and Tool usage:
- IDE: Pycharm Community Edition
- Environment: Conda
- Version Control: Github
- Project Management: Zenhub
- Communication: Discord

### Milestone 3 Roles:
- Matt Gubler - Programmer
- Kevin Pett - Scrum Master
- Michael Short - Recorder
- Aidan Dougherty - Product Owner

### Milestone 1-2 Roles:
- Matt Gubler - Product Owner
- Kevin Pett - Recorder
- Michael Short - Scrum Master
- Aidan Dougherty - Programmer
