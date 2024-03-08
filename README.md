# information-resource-registry

The information resource registry is a listing of data sources present in the NCATS Data Translator system.  Each information resource has an identifier, a short description, and an URL to more information about that resource.

## Website

[https://biolink.github.io/information-resource-registry](https://biolink.github.io/information-resource-registry)

## Repository Structure

* [examples/](examples/) - example data
* [project/](project/) - project files (do not edit these)
* [src/](src/) - source files (edit these)
  * [information_resource_registry](src/information_resource_registry)
    * [schema](src/information_resource_registry/schema) -- LinkML schema
      (edit this)

## Developer Documentation

<details>
Use the `make` command to generate project artefacts:

* `make all`: make everything
* `make deploy`: deploys site
</details>

## Credits

This project was made with
[linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter).
