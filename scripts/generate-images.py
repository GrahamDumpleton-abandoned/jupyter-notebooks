'''
Generates the image stream resource definitions.

'''

import powershift.resources as resources

image_stream = resources.v1_ImageStream(
    metadata = resources.v1_ObjectMeta(
        name = 'jupyter-notebook',
        annotations = {
          'openshift.io/display-name': 'Jupyter Notebook'
        }
    ),
    spec = resources.v1_ImageStreamSpec()
)

image_stream.spec.tags.append(
    resources.v1_TagReference(
        name = '2.7',
        annotations = {
          'openshift.io/display-name': 'Jupyter Notebook (Python 2.7)',
          'description': 'Build and deploy custom Jupyter Notebook images for Python 2.7.',
          'iconClass': 'icon-python',
          'tags': 'builder,python,jupyter',
          'supports':'python',
          'version': '2.7',
          'sampleRepo': 'https://github.com/ricardoduarte/python-for-developers.git'
        },
        from_ = resources.v1_ObjectReference(
            kind = 'DockerImage',
            name = 'getwarped/s2i-notebook-python27:latest'
        )
    )
)

image_stream.spec.tags.append(
    resources.v1_TagReference(
        name = '3.5',
        annotations = {
          'openshift.io/display-name': 'Jupyter Notebook (Python 3.5)',
          'description': 'Build and deploy custom Jupyter Notebook images for Python 3.5.',
          'iconClass': 'icon-python',
          'tags': 'builder,python,jupyter',
          'supports':'python',
          'version': '3.5',
          'sampleRepo': 'https://github.com/ricardoduarte/python-for-developers.git'
        },
        from_ = resources.v1_ObjectReference(
            kind = 'DockerImage',
            name = 'getwarped/s2i-notebook-python35:latest'
        )
    )
)

image_stream.spec.tags.append(
    resources.v1_TagReference(
        name = 'latest',
        annotations = {
          'openshift.io/display-name': 'Jupyter Notebook (Python 3.X)',
          'description': 'Build and deploy custom Jupyter Notebook images for Python 3.X.',
          'iconClass': 'icon-python',
          'tags': 'builder,python,jupyter',
          'supports':'python',
          'sampleRepo': 'https://github.com/ricardoduarte/python-for-developers.git'
        },
        from_ = resources.v1_ObjectReference(
            kind = 'ImageStreamTag',
            name = '3.5'
        )
    )
)

resources.dump(image_stream, indent=4, sort_keys=True)
