import logging
import time

from source.configuration_setup import Configuration
from source.output_management import (
    copy_config_file,
    remove_temp_files,
    set_up_output_directory,
)
from source.parameter_generation import generate_parameters
from source.turbospectrum_integration.compilation import (
    compile_interpolator,
    compile_turbospectrum,
)
from source.turbospectrum_integration.interpolation import (
    create_template_interpolator_script,
)
from source.turbospectrum_integration.run_turbospectrum import generate_all_spectra
from source.turbospectrum_integration.utils import collect_model_atmosphere_parameters


def main():
    # TODO: Add functionality to read path from commandline
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    start_time = time.time()

    try:
        # Initialize configuration
        config = Configuration()

        # Set up output directory
        set_up_output_directory(config)

        # Copy configuration file to output directory for reference
        copy_config_file(config)

        # Load model atmospheres
        model_atmospheres = collect_model_atmosphere_parameters(
            config.path_model_atmospheres
        )

        # Generate stellar parameters
        stellar_parameters = generate_parameters(config)

        # Compile Turbospectrum and interpolator
        compile_turbospectrum(config)
        compile_interpolator(config)

        # Create template for interpolator script
        create_template_interpolator_script(config)
    except Exception as e:
        logging.error(f"Error during setup: {e}")
        raise e

    # Generate all spectra
    generate_all_spectra(config, model_atmospheres, stellar_parameters)

    # Remove temporary files
    # Toggle the function call below to access scripts
    # and intermediate files used during the process
    # remove_temp_files(config)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Total execution time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
