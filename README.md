# Password Manager

This is a local password manager designed to securely store and manage your passwords with ease. It uses an encrypted JSON file to save the data locally on your machine. It comes with a range of features including password validation, search, and a master password for added security.

1. [Features](#features)
1. [Installation](#installation)
1. [Contributing](#contributing)
1. [Future Improvements](#future-improvements)
1. [License](#license)

## Features

- **Graphical User Interface**: A user-friendly interface for password management.
- **Master Password Protection**: A password is required to access the application.
- **Website & Password Form**:
  - Input for website url/name.
  - Input for email, auto-filled with [username]@gmail.com
  - Input for password with an option to generate a strong password.
  - By default, copy the generated password to the clipboard.
  - Form validations to ensure data integrity and security.
- **Password Encryption**: Passwords are encrypted & stored in the JSON file & decrypted when needed.
- **Save Functionality**: A save button to save the entered data, followed by clearing the form.
- **Multiple Accounts**: Ability to store & handle multiple accounts for the same website.
- **Search Functionality**: A search feature to look up & display the saved website data.
- **Edit & Delete Options**: Ability to edit or delete website details after a confirmation step.

## Installation

- Clone the repository: `git clone https://github.com/siddhant-vij/Password-Manager.git`
- Navigate to the project directory: `cd Password-Manager`
- Delete the following files:
  - `data/masterHash`
  - `data/passwords.json.enc`
  - `resources/hashSalt`
- Install dependencies: `conda create --name password-manager --file requirements.txt`
- Activate the environment: `conda activate password-manager`
- Install remaining dependencies: `pip install pyperclip`
- Run the application: `python main.py`

## Contributing

All contributions to this project are welcome. If you have suggestions or want to contribute to the codebase, please follow the steps below:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## Future Improvements
- **Command-Line Interface**: Offer a CLI for advanced users to manage their passwords without a GUI.
- **Auto-Logout Timer**: An auto-logout mechanism that secures the application when it's inactive for a certain period.
- **Two-Factor Authentication**: Enhance security using methods like a mobile authenticator app or email confirmation.
- **Backup Recovery**: Option to back up encrypted password databases and facilitate easy recovery in case of data loss.
- **Audit Logs**: Keep track of changes with an audit log feature to monitor when entries are added, modified, or deleted.
- **Security Notifications**: Send alerts passwords need to be changed due to potential leaks found in data breaches.
- **User-Defined Categories**: Allow users to create custom categories for organizing their passwords.
- **Secure Notes**: Apart from passwords, offer templates for securely storing notes, credit card information, etc.
- **Security Policies**: Let users set custom policies, like minimum password length, expiration time, etc.
- **Cross-Platform Compatibility**: Ensure the application works seamlessly across different operating systems and devices.
- **Cloud Synchronization**: Implement cloud storage options to sync password data across multiple devices securely.
- **Browser Extension**: That can autofill login forms and capture new login details directly from the web browser.


## License

Distributed under the MIT License. See [LICENSE](https://github.com/siddhant-vij/Password-Manager/blob/main/LICENSE) for more information.