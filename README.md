# S2I Enabled Jupyter Notebook Images

This repository provides templates and documentation for deploying [Source-to-Image](https://github.com/openshift/source-to-image) (S2I) enabled [Jupyter Notebook](http://jupyter.org) images on OpenShift.

## Comparison to Jupyter Project Images

The Jupyter project provides Docker-formatted container images via their [GitHub project](https://github.com/jupyter/docker-stacks) and on [Docker Hub](https://hub.docker.com/u/jupyter/).

The images that the Jupyter project provides will not work with the default security profile of OpenShift. This is because the Jupyter project images, although they have attempted to set them up so they do not run as ``root``, will not run in a multi tenant PaaS environment where any container a user runs is forced to run with an assigned ``uid`` different to that specified by the image.

The issues preventing the Jupyter project images being able to be run in a default installation of OpenShift have been [reported](https://github.com/jupyter/docker-stacks/issues/188) via the GitHub project but at this point have not been addressed.

To address those issues, the images which can be built from this repository are a layer on top of the Jupyter project images and apply the required fixes to the base images to enable them to work on OpenShift without having to override the default security profile of the OpenShift installation.

The images here have also been S2I enabled to provide an easy way of binding source files, including notebooks, Python code files and data files, with an image and deploy it to OpenShift. The build process using S2I can also install additional Python modules required by a user to run their notebooks.

To make use of OpenShift's ability to easily spin up multiple applications and processes, the images have also been extended to add support for doing parallel computing using the ``ipyparallel`` package.

## List of Customised Images Available

At this point, this project has a focus on providing customised images for working in Python using the Jupyter notebooks. The images which are available are:

* getwarped/s2i-minimal-notebook - ([GitHub Repository](https://github.com/getwarped/s2i-minimal-notebook), [Docker Hub](https://hub.docker.com/r/getwarped/s2i-minimal-notebook/))
* getwarped/s2i-scipy-notebook - ([GitHub Repository](https://github.com/getwarped/s2i-scipy-notebook), [Docker Hub](https://hub.docker.com/r/getwarped/s2i-scipy-notebook/))
* getwarped/s2i-tensorflow-notebook ([GitHub Repository](https://github.com/getwarped/s2i-tensorflow-notebook), [Docker Hub](https://hub.docker.com/r/getwarped/s2i-tensorflow-notebook/))

Variants of other Jupyter project images including support for other languages aren't being provided.

Do be aware that the Jupyter project base images are very large. The first time you attempt to deploy one, it may take some time as it is downloaded and then pushed out to the node your application is deployed on.

## Deploying the Customised Images

The easiest way to deploy these Jupyter notebook images and get working is to import which of the above images you wish to use and then use the OpenShift templates provided with this project to deploy them.

To import all the above images into your project, you can run the ``oc import-image`` command.

```
oc import-image getwarped/s2i-minimal-notebook --confirm
oc import-image getwarped/s2i-scipy-notebook --confirm
oc import-image getwarped/s2i-tensorflow-notebook --confirm
```

This should result in the creation of three image streams within your project.

```
s2i-minimal-notebook
s2i-scipy-notebook
s2i-tensorflow-notebook
```

You could deploy the images directly, but the templates provide an easier way of setting a password for your notebooks, and will also ensure that a secure HTTP connection is used when interacting with the notebook interface.

To load the OpenShift templates you can run the ``oc create`` command.


```
oc create -f https://raw.githubusercontent.com/getwarped/s2i-jupyter-stacks/master/templates.json
```

This should create three templates within your project. The purpose of each template is as follows:

* ``jupyter-notebook`` - Deploy a notebook server from an image stream. This can be one of the standard images listed above, or a customised image which has been created using the ``jupyter-builder`` template. The notebook can optionally be linked to a parallel compute cluster created using ``jupyter-cluster``.

* ``jupyter-builder`` - Create a customised notebook image. This will run the S2I build process, starting with any of the standard images, or even a customised image, to bind additional files into the image. This can be used to incorporate pre-defined notebooks, data files, or install additional Python packages.

* ``jupyter-cluster`` - Deploy a parallel compute cluster comprising of a controller and single compute engine. The number of compute engines can be scaled up to as many as necessary.

## Deploying the Notebook Server

To deploy a notebook server, select _Add to Project_ from the web console and enter ``jupyter`` into the search filter. Select ``jupyter-notebook``.

![image](images/add_to_project_jupyter_notebook.png)

On the page for the ``jupyter-notebook`` template fill in the name of the application, the name of the image you wish to deploy (defaults to ``s2i-scipy-notebook``) and a password for the notebook server. Also override the ``app`` label applied to resources created when deploying the notebook server with a unique name. This will make it easier to delete the notebook server later.

![image](images/create_jupyter_notebook.png)

If you do not provide your own password, a random password will be used. You can find out the name of the generated password by going to the _Environment_ tab of the _Deployments_ page for your notebook server in the OpenShift web console.

Once created the notebook server will be deployed and automatically exposed via a route to the Internet over a secure HTTP connection. You can find the URL it is exposed as from the _Overview_ page for your project.

![image](images/overview_notebook.png)

When you visit the URL you will be prompted for the password you entered via the template to get access to the notebook server.

If you use any of the ``s2i-minimal-notebook``, ``s2i-scipy-notebook`` or ``s2i-tensorflow-notebook`` images in the ``NOTEBOOK_IMAGE`` field of the template, you will be presented with an empty work directory. You can create new notebooks or upload your own as necessary.

Do note that by default any work you do is not being saved in a persistent volume. Thus if the notebook server is restarted at any point by you explicitly, or by OpenShift, your work will be lost.

To enable you to preserve your work, even if the notebook server is restarted, you should attach a persistent storage volume to the notebook server. This can be done from the _Deployments_ page for your notebook server.

![image](images/deployments_attach_storage_notebook.png)

The mount path for the storage should be set to be ``/home/jovyan/work``.

![image](images/attach_storage_notebook.png)

The storage should be attached before you do anything else. The notebook server will be automatically restarted when you make the storage request.

When done with your work, you can download your files using the Jupyter notebook interface. Alternatively, you can use the ``oc rsync`` command to copy files from your application back to your local computer.

To delete the Jupyter notebook server when no longer required, you can use the ``oc delete all --selector app=<name>`` command, where ``<name>`` is replaced with the value you gave the ``app`` label in the template page when deploying the Jupyter notebook server.

Note that when the application is deleted, the persistent storage volume will not be deleted. To delete that you should determine the name of the persistent storage volume using ``oc get pvc`` and then delete it using ``oc delete pvc/<name>``.