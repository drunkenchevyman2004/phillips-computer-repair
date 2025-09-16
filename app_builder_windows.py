"""
app_builder_windows.py

This script implements a simple graphical interface to help non‑technical users scaffold 
mobile app projects that can be published to the Apple App Store.  It runs on Windows
systems and uses only the built‑in `tkinter` library, so there is no need to install
external GUI frameworks.  The tool guides you through entering some basic details
about your app, uploading image assets, enabling a simple paywall placeholder and
choosing whether your idea is a tool or a game.  When you click **Generate Project**, 
the script creates a directory for the new app and populates it with a minimal
cross‑platform project skeleton along with the assets you provided.  Although this
program cannot compile an iOS app on its own (Apple’s build tools require macOS),
the generated files give you a structured starting point that you can open in
Flutter, React Native or another framework on a Mac.

Key features:

* **User‑friendly GUI:** Uses Tkinter to present a straightforward form for
  entering the app name, selecting the app type (Tool or Game) and toggling a
  paywall option.
* **Image upload:** Lets you select one or more image files from your computer
  (icons, screenshots, artwork).  These files are copied into the new project’s
  `assets/images` folder.
* **Paywall scaffolding:** When enabled, a placeholder file and code comments
  are added to the project to remind you to implement in‑app purchases using
  Apple’s StoreKit or your preferred cross‑platform in‑app purchase library.
* **Project skeleton:** Creates a minimal project directory with a README
  explaining how to continue building and publishing your app.  Also generates a
  simple `main.dart` file using Flutter conventions to display the uploaded
  images and (optionally) a paywall screen.
* **Export to ZIP:** Optionally packages the generated project directory into a
  zip archive for easy sharing or transfer to another machine.

Usage:

Run the script on a Windows machine with Python installed:

```
python app_builder_windows.py
```

The GUI will open in a window.  Fill in the fields, select your assets and click
**Generate Project**.  The output folder will be created in the same directory as
the script unless you specify a custom location.
"""

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import zipfile


class AppBuilderGUI:
    """Graphical interface for scaffolding simple app projects."""

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("App Builder for Apple App Store")
        self.assets = []

        # Create and lay out widgets
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Initialize and arrange GUI components."""
        padding_x = 10
        padding_y = 5

        # App name
        tk.Label(self.master, text="App Name:").grid(row=0, column=0, sticky="w", padx=padding_x, pady=padding_y)
        self.app_name_var = tk.StringVar()
        tk.Entry(self.master, textvariable=self.app_name_var, width=40).grid(row=0, column=1, padx=padding_x, pady=padding_y)

        # App type selection
        tk.Label(self.master, text="App Type:").grid(row=1, column=0, sticky="w", padx=padding_x, pady=padding_y)
        self.app_type_var = tk.StringVar(value="Tool")
        tk.OptionMenu(self.master, self.app_type_var, "Tool", "Game").grid(row=1, column=1, sticky="w", padx=padding_x, pady=padding_y)

        # Paywall checkbox
        self.paywall_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.master, text="Include Paywall", variable=self.paywall_var).grid(row=2, column=1, sticky="w", padx=padding_x, pady=padding_y)

        # Image upload button and list
        tk.Button(self.master, text="Upload Images", command=self.upload_images).grid(row=3, column=0, padx=padding_x, pady=padding_y)
        self.images_listbox = tk.Listbox(self.master, height=4, width=40)
        self.images_listbox.grid(row=3, column=1, padx=padding_x, pady=padding_y)

        # Output directory selection
        tk.Label(self.master, text="Output Directory:").grid(row=4, column=0, sticky="w", padx=padding_x, pady=padding_y)
        self.output_dir_var = tk.StringVar(value=os.getcwd())
        tk.Entry(self.master, textvariable=self.output_dir_var, width=40).grid(row=4, column=1, padx=padding_x, pady=padding_y)
        tk.Button(self.master, text="Browse", command=self.browse_output_directory).grid(row=4, column=2, padx=padding_x, pady=padding_y)

        # Generate project button
        tk.Button(self.master, text="Generate Project", bg="green", fg="white", command=self.generate_project).grid(
            row=5, column=1, pady=padding_y, padx=padding_x, sticky="ew"
        )

    def upload_images(self) -> None:
        """Open a file dialog to select image files and add them to the list."""
        files = filedialog.askopenfilenames(
            parent=self.master,
            title="Choose images",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("All files", "*.*")],
        )
        for file in files:
            if file not in self.assets:
                self.assets.append(file)
                self.images_listbox.insert(tk.END, os.path.basename(file))

    def browse_output_directory(self) -> None:
        """Open a directory chooser for selecting the output directory."""
        directory = filedialog.askdirectory(parent=self.master, title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)

    def _sanitize_name(self, name: str) -> str:
        """Return a filesystem‑safe version of the app name."""
        return "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')

    def generate_project(self) -> None:
        """Create the app project structure and copy selected assets."""
        name = self.app_name_var.get().strip()
        if not name:
            messagebox.showerror("Missing Information", "Please provide an app name.")
            return

        # Determine output directory and ensure it exists
        base_output = self.output_dir_var.get().strip()
        if not base_output:
            messagebox.showerror("Invalid Directory", "Please specify a valid output directory.")
            return

        safe_name = self._sanitize_name(name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = os.path.join(base_output, f"{safe_name}_{timestamp}")
        try:
            os.makedirs(project_dir, exist_ok=False)
        except Exception as e:
            messagebox.showerror("Directory Error", f"Unable to create project directory:\n{e}")
            return

        # Create subdirectories
        assets_dir = os.path.join(project_dir, "assets", "images")
        os.makedirs(assets_dir, exist_ok=True)
        lib_dir = os.path.join(project_dir, "lib")
        os.makedirs(lib_dir, exist_ok=True)

        # Copy image assets
        for img_path in self.assets:
            try:
                shutil.copy(img_path, os.path.join(assets_dir, os.path.basename(img_path)))
            except Exception as e:
                messagebox.showwarning("Asset Copy Error", f"Failed to copy {img_path}: {e}")

        # Generate main.dart
        main_dart_path = os.path.join(lib_dir, "main.dart")
        with open(main_dart_path, "w", encoding="utf-8") as f:
            f.write(self._generate_main_dart_code(name, self.app_type_var.get(), self.paywall_var.get(), self.assets))

        # Create pubspec.yaml referencing assets
        pubspec_path = os.path.join(project_dir, "pubspec.yaml")
        with open(pubspec_path, "w", encoding="utf-8") as f:
            f.write(self._generate_pubspec_yaml(self.assets))

        # Create README with instructions
        readme_path = os.path.join(project_dir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(self._generate_readme(name))

        # Add placeholder for paywall if needed
        if self.paywall_var.get():
            paywall_file = os.path.join(project_dir, "PAYWALL.txt")
            with open(paywall_file, "w", encoding="utf-8") as f:
                f.write(
                    "This project includes a placeholder for implementing a paywall.\n"
                    "To enable in‑app purchases on iOS, you will need to integrate Apple’s StoreKit.\n"
                    "If you choose a cross‑platform framework like Flutter, add the `in_app_purchase`\n"
                    "package in your pubspec.yaml and follow the documentation to configure products\n"
                    "in App Store Connect.\n"
                )

        # Optionally zip the project (ask user)
        if messagebox.askyesno("Zip Project?", "Do you want to package the project into a ZIP archive?"):
            zip_name = f"{safe_name}_{timestamp}.zip"
            zip_path = os.path.join(base_output, zip_name)
            self._zip_directory(project_dir, zip_path)

        messagebox.showinfo("Success", f"Project generated successfully at:\n{project_dir}")

    def _zip_directory(self, dir_path: str, zip_path: str) -> None:
        """Create a ZIP archive of the specified directory."""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(dir_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, start=os.path.dirname(dir_path))
                    zipf.write(full_path, rel_path)

    def _generate_main_dart_code(self, app_name: str, app_type: str, include_paywall: bool, assets: list) -> str:
        """Return a string containing a minimal Flutter `main.dart` file."""
        # List asset image names for demonstration
        image_widgets = []
        for img_path in assets[:3]:  # limit to first three images for preview
            image_name = os.path.basename(img_path)
            image_widgets.append(
                f"          Image.asset('assets/images/{image_name}', width: 200, height: 200),"
            )
        images_code = "\n".join(image_widgets) if image_widgets else "          Text('No images uploaded'),"

        paywall_code = ""
        if include_paywall:
            paywall_code = (
                "\n      ElevatedButton(\n        onPressed: () {\n          // TODO: Implement paywall logic and call StoreKit or your preferred in-app purchase API\n        },\n        child: const Text('Unlock premium'),\n      ),"
            )

        return f"""
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {{
  const MyApp({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: '{app_name}',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const HomePage(),
    );
  }}
}}

class HomePage extends StatelessWidget {{
  const HomePage({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(title: const Text('{app_name}')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
{images_code}
            const SizedBox(height: 20),
            Text('This is a {app_type.lower()} app built with App Builder!', style: const TextStyle(fontSize: 18)),{paywall_code}
          ],
        ),
      ),
    );
  }}
}}
"""

    def _generate_pubspec_yaml(self, assets: list) -> str:
        """Generate a Flutter pubspec.yaml file listing the assets."""
        asset_paths = [f"    - assets/images/{os.path.basename(img)}" for img in assets]
        assets_block = "\n".join(asset_paths) if asset_paths else ""
        return f"""
name: example_app
description: A simple project scaffold generated by App Builder.
publish_to: none
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.6

dev_dependencies:
  flutter_test:
    sdk: flutter

flutter:
  uses-material-design: true
  assets:
{assets_block}
"""

    def _generate_readme(self, app_name: str) -> str:
        """Create a README explaining next steps for the generated project."""
        return f"""
# {app_name}

This project was generated using the App Builder for Windows.  It provides a
minimal Flutter scaffold that displays any images you uploaded and includes
optional paywall placeholders.  To continue building and publishing your app to
the Apple App Store, follow these steps:

1. **Install Flutter:** If you haven’t already, download and install Flutter from
   [flutter.dev](https://flutter.dev).  Make sure you can run `flutter doctor` without
   errors on your system.
2. **Move project to macOS:** To build and publish an iOS app, you will need a
   Mac with Xcode installed.  Copy this project to a Mac or use a cloud
   continuous‑integration service that provides macOS build agents.
3. **Add dependencies:** Open the `pubspec.yaml` file and add any additional
   packages your app requires.  For paywalls, consider packages like
   `in_app_purchase`.
4. **Implement functionality:** Edit `lib/main.dart` and other Dart files to
   implement your tool or game logic.  Replace the placeholder code with your
   actual user interface and business logic.
5. **Configure app:** Update the Flutter project’s bundle identifier, icons and
   other metadata in the iOS `Runner` Xcode project.  You can find more details
   in the Flutter documentation.
6. **Test and publish:** Use `flutter build ios` to produce an iOS build.
   Then open the generated Xcode workspace, run your app on a simulator or
   device, fix any issues and submit through App Store Connect.

Enjoy building your app!
"""


def main() -> None:
    root = tk.Tk()
    gui = AppBuilderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
