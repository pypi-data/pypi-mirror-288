#Digixt_pipeline_template_plugin_builder

## Prerequesit 
Ensure Python is installed and available by running:
``` python3 --version ```
## Create and Install the Plugin
### Create a Source Distribution Package:

Run the following command to create the source distribution package. It will be generated in the dist/ folder of your current working directory:

``` python3 setup.py sdist  ```
#### Optional: Move the Distribution Package:

If you need to move the generated archive file (digixt-pipeline-template-1.0.tar.gz, replace 1.0 with your actual version) to another location, use the mv command:

``` mv dist/digixt-pipeline-template-1.0.tar.gz /path/to/destination ```

### Install the Plugin:

Install the plugin using pip. Navigate to the directory where the distribution archive is located (either in dist/ or your specified destination):

``` pip install /path/to/digixt-pipeline-template-1.0.tar.gz ```
#### Verify Installation:

Check if the plugin is installed correctly by listing installed packages:

``` pip list ```

You should see digixt-pipeline-template in the list.

## Usage
To use the plugin and create a template PySpark project structure, run the following command:

``` digixt-pipeline-template --name <my-project-name> ```

Replace <my-project-name> with your desired project name.