import argparse
import os
from .project_structure_generator import ProjectStructureGenerator, CommonLogging


def main():
    parser = argparse.ArgumentParser(
        description='Create a PySpark project structure template',
        usage='%(prog)s -name PROJECT_NAME'
    )
    parser.add_argument(
        '-name', '--name',
        required=True,
        help='Name of the project (must be at least three characters and a valid Python identifier)'
    )

    args = parser.parse_args()
    project_name = args.name
    
    # validate project name
    if not  (project_name  and len(project_name) >= 3 and project_name.replace('-', '_').isidentifier()):
        raise ValueError("Invalid Project Name: Project Name must be greater than or equal to three in length!")

    logging = CommonLogging.get_logger()
    try:
        logging.info(f"PySpark project structure generator '{project_name}'...")
        ProjectStructureGenerator.copy_and_rename_template(project_name)
        configs, full_config_file_path = ProjectStructureGenerator.read_config_file(project_name)
        configs = ProjectStructureGenerator.update_template_by_project_name(configs, full_config_file_path, project_name)
        ProjectStructureGenerator.write_to_config_file(configs, full_config_file_path)

        logging.info("Project structore creation complete.")
    except Exception as e:
        logging.error(f"Some thing went wrong while creating the project structure: {str(e)}")
        raise

if __name__ == "__main__":
    main()
