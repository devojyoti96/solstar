
# SOLSTAR : SOLar Simulation of Thermal and Active Radio emissions

**SOLSTAR** (**SOL**ar **S**imulation of **T**hermal and **A**ctive **R**adio emissions) is a simulation tool for simulating solar radio emissions at GHz frequencies. It is designed to simulate spectral image cube at user given frequency range and frequency resolution at any observation date based on extreme ultraviolet observations of the Sun.

---

## 🌟 Features

- **GHz Frequency Simulation**: Simulate solar radio emissions in the GHz range.
- **Visibility simulation**: Simulate visibility of a given radio interferometric array.
- **Customizable Parameters**: Configure frequency ranges, frequency and temporal resolutions, and spatial resolution. 
- **Data Export**: Export simulation images in FITS and visibilities in CASA measurement format.
- **Modular Architecture**: Integrates seamlessly with other solar physics tools and workflows.

---

## 🚀 Installation

To install and set up **SOLSTAR**, follow these steps:

### Prerequisites
- Python 3.10 or higher
- Git
- Required Python libraries (listed in `requirements.txt`)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/devojyoti96/solstar.git
   cd solstar
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Preview parameters of the application:
   ```bash
   run_solstar -h
   ```
   
4. Launch the application:
   ```bash
   run_solstar 
   ```
---

## 🛠️ Usage

### Basic Simulation
1. Edit the configuration file (`config.json`) to specify your simulation parameters:
   - Frequency range (e.g., `1 GHz - 10 GHz`)
   - Time intervals
   - Solar activity models
2. Run the simulation:
   ```bash
   python starsim.py --config config.json
   ```
3. Access the results in the `output/` folder.

### Advanced Options
- Enable real-time visualization:
  ```bash
  python starsim.py --visualize
  ```
- Export data in a specific format (e.g., FITS):
  ```bash
  python starsim.py --output-format fits
  ```
- Debug mode for detailed logs:
  ```bash
  python starsim.py --debug
  ```

---

## 📖 Documentation

For detailed documentation, including parameter definitions, examples, and advanced configuration guides, visit the [STARSIM Documentation](https://your-documentation-url.com).

---

## 🤝 Contributing

Contributions to **STARSIM** are welcome! Here’s how you can help:
1. Fork the repository.
2. Create a branch for your feature or fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push:
   ```bash
   git commit -m "Description of feature"
   git push origin feature-name
   ```
4. Submit a pull request for review.

Please ensure your contributions align with our coding standards and include relevant documentation.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

- Developed by the **Devojyoti Kansabanik** and **Surajit Mondal**.
- Inspired by cutting-edge advancements in GHz solar radio spectral analysis.
- Special thanks to developers of  and the scientific community for their support.

---

## 📬 Contact

For questions, feature requests, or support:
- **Email**: dkansabanik@ucar.edu
- **GitHub Issues**: [https://github.com/devojyoti96/solstar/issues](https://github.com/your-repo/STARSIM/issues)

---

**SOLSTAR** is your gateway to understanding solar radio emissions at GHz frequencies. Start exploring today! 🌞

