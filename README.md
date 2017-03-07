# hello-gbdx

A GBDX task that obtains a list of the task input files and prints this list in the file out.txt, along with a user defined message.

## Run

Here we run a sample execution of the hello-gbdx task. Sample inputs are provided on S3 in the locations specified below.

1. In a Python terminal create a GBDX interface and specify the task input location:

    ```python
    from gbdxtools import Interface
    from os.path import join
    import uuid

    gbdx = Interface()

    input_location = 's3://gbd-customer-data/58600248-2927-4523-b44b-5fec3d278c09/platform-stories/hello-gbdx'
    ```

2. Create a task instance and set the required inputs:

    ```python
    # create task object
    hello_task = gbdx.Task('hello-gbdx')
    hello_task.inputs.data_in = join(input_location, 'data_in')
    hello_task.inputs.message = 'This is my message!'
    ```

3. Initialize a workflow and specify where to save the output:

    ```python
    # Define a single-task workflow
    workflow = gbdx.Workflow([hello_task])
    random_str = str(uuid.uuid4())
    output_location = join('platform-stories/trial-runs', random_str)

    workflow.savedata(hello_task.outputs.data_out, output_location)
    ```

4. Execute the workflow and track it's status as follows:

    ```python
    workflow.execute()
    workflow.status
    ```

## Input Ports

The task input ports. GBDX input ports can only be of "Directory" or "String" type. Note that booleans, integers and floats <b>must be</b> passed to the task as strings, e.g., "True", "10", "0.001".

| Name  | Type | Description | Required |
|---|---|---|---|
| message | string | A user-defined message. | True |
| data_in | directory | Input data directory. | True |


## Output Ports

| Name  | Type | Description |
|---|---|---|  
| data_out | directory | Output data directory. Contains out.txt, which has a list of files in data_in and the user-defined message. |

## Development

### Build the Docker Image

You need to install [Docker](https://docs.docker.com/engine/installation).

Clone the repository:

```bash
git clone https://github.com/platformstories/hello-gbdx
```

Then

```bash
cd hello-gbdx
docker build -t hello-gbdx .
```

### Try out locally

Create a container in interactive mode and mount the sample input under `/mnt/work/input/`:

```bash
docker run -v full/path/to/sample-input:/mnt/work/input -it hello-gbdx
```

Then, within the container:

```bash
python /hello-gbdx.py
```

### Docker Hub

Login to Docker Hub:

```bash
docker login
```

Tag your image using your username and push it to DockerHub:

```bash
docker tag hello-gbdx yourusername/hello-gbdx
docker push yourusername/hello-gbdx
```

The image name should be the same as the image name under containerDescriptors in hello-gbdx.json.

Alternatively, you can link this repository to a [Docker automated build](https://docs.docker.com/docker-hub/builds/). Every time you push a change to the repository, the Docker image gets automatically updated.
### Register on GBDX

In a Python terminal:
```python
from gbdxtools import Interface
gbdx=Interface()
gbdx.task_registry.register(json_filename="hello-gbdx.json")
```

Note: If you change the task image, you need to reregister the task with a higher version number in order for the new image to take effect. Keep this in mind especially if you use Docker automated build.
