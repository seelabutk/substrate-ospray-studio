# Project Description

In this project, your goal is to set up a cloud-based rendering service, or a Rendering as a Service (RaaS), using Amazon AWS running OSPRay Studio.
You will use concepts and tools that were first proposed and tested out through Visualization as a Service (VaaS) research that started around 2015 at the University of Tennessee, Knoxville with funding from NSF and Intel.

Specifically, you will use Substrate, which is our latest effort to consolidate the tools needed to create a VaaS or a RaaS. The back-end rendering engine you will use is OSPRay. Both Substrate and OSPRay Studio are open source:
  - Substrate: https://github.com/seelabutk/substrate
  - OSPRay Studio: https://github.com/ospray/ospray_studio

After setting up the RaaS, your next tasks are to build a scene, build a front-end UI in a web browser using Javascript so that you can interact with the scene, and then create a movie by setting and controlling key frames. The specific requirements are as follows.

### Step 1 - Set up the RaaS

1. Set up your own AWS account. Go to https://aws.amazon.com/ and create a new free-tier account. You should not need to use any resources that don't qualify for the free-tier.

2. Follow [this guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/howtogetcredentials.html) to get your CLI credentials for AWS, and ensure they are available for the next steps.

3. Follow [this guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to install the AWS CLI.

4. Install [Node and NPM](https://nodejs.org/en/download/). Then run the following command to install the AWS CDK CLI:

    ```npm install aws-cdk@^1.147.0```

5. Install [Python 3.8](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/).

6. Install Substrate with `pip install seelabutk-substrate`.

7. Define the configuration for Substrate. This can be done by creating a file called `substrate.config.yaml` in your working directory. An example config that will load a simple demo is included with this repo.
For more information on the full options available to you, please see the [configuration API](https://github.com/seelabutk/substrate/blob/main/api/substrate.config.yaml).

8. Run the following command to deploy your RaaS to AWS:

    ```substrate ospray_studio start```

9. The previous command should output a link where your RaaS can be accessed.

TODO: screenshot of link output here

Once your RaaS has had time to complete setup (this may take 10-15 minutes), open that link and ensure that you can see the default OSPRay Studio scene display.
If your RaaS launched successfully, you should see a rendering of an apple.

TODO: screenshot of apple here

10. To kill your RaaS, run the following command:

    ```substrate ospray_studio stop```

The RaaS includes an API which can be used to submit rendering requests and get images or movies back. If the link outputted by your RaaS was http://127.0.0.1, then the following endpoints will be available to you:

    - http://127.0.0.1/ - This is the endpoint that will serve a rendering of the objects specified in `substrate.config.yaml` to ensure the RaaS is available and working. You should open this endpoint in a browser after the RaaS has launched.
    - http://127.0.0.1/sg - Returns the SceneGraph that was used to perform the first rendering by the RaaS. This will not work until the previous endpoint has been opened in a browser.
    - http://127.0.0.1/render - Takes a SceneGraph as input and returns a PNG of the newly rendered frame. This should primarily be used to identify suitable SceneGraphs for use as key frames by the following endpoint.
    - http://127.0.0.1/renderMovie - Takes multiple SceneGraphs treated as key frames as input and returns a movie animating the scene through these key frames.
    - TODO: Expose number of samples and resolution.

You can interact with these endpoints in a browser through the use of the Fetch API. Examples of how to use the Fetch API to communicate with each endpoint can be seen in the JavaScript file in the skeleton code for this project.
More details on the Fetch API can be found [here](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch).

### Step 2 - Add your own objects to the scene

Start by going to [Poly Haven](https://polyhaven.com/models) and grabbing at least three objects to put in your scene instead of the apple. Make sure you download GLTF files to ensure compatibility with OSPRay Studio.

Next, modify the `data.source` option in `substrate.config.yaml` to point to the directory containing these three files.

Now, repeat parts 8 & 9 of Step 1 to get a simple rendering with each of the objects in the scene. This will likely look poor or even chaotic, and you will next need to configure OSPRay Studio in order to improve it.

### Step 3 - Run the skeleton code

TODO: James how do you want them to host their skeleton code locally? I'll give them an HTML file with JSON Editor loaded and JS which will do an initial render of the objects with no configuration.

### Step 4 - Use jsoneditor to modify the SceneGraph

Before beginning this step, take the skeleton code and modify the RAAS_LOCATION variable in `raas.js` to point to your RaaS.

OSPRay Studio is configured through what is referred to as a SceneGraph (.sg file). This is a JSON-formatted file that contains the information necessary to perform an OSPRay rendering.
You may retrieve the SceneGraph used to render the initial scene through the endpoint at {your_raas_link}/sg.

Once you have the SceneGraph, changes can be made to the scene by editing the JSON and issuing a new rendering request to the RaaS.

To edit the SceneGraph, we have included [JSON Editor](https://github.com/josdejong/jsoneditor) in the skeleton code for this project. Here is an example of how it could look once incorporated into your UI.

TODO: screenshot of JSON Editor here

To use the edited SceneGraph to produce a new rendering, send a POST request to {your_raas_link}/render that contains your new SceneGraph in the request body.
The response from the server, if your SceneGraph is valid, will be a PNG-formatted image with the newly-rendered frame. An example of how this works is included in the skeleton code.

In order to complete this step, modify the SceneGraph with JSON Editor to move the objects and the camera such that the scene is well-organized. Note that in order to manipulate the camera, you should use the
`camera.position`, `camera.up`, and `camera.view` vectors.

### Step 5 - Add functionality to your browser UI to create movies

The RaaS also supports the creation of movies. To do so, you may save multiple SceneGraphs with different parameters (such as the camera position) as key frames, and then send them via a POST request to {your_raas_link}/renderMovie.
The RaaS will perform a linear interpolation between each key frame and produce an AV1-encoded .mp4 file with the request length and frame rate. The format of the body of your POST request should look as follows:

    {
      frames: Array of SceneGraphs to use as key frames,
      fps: your desired fps,
      length: your desired video length in seconds
    }

This process may be slow due to the need to render large numbers of frames, so consider beginning with something small such as a 2-second, 10-fps video. Also, please note that the video may not exactly match your desired length and frame rate after being encoded.

### Grading criteria

  - Step 1: 30 points
  - Step 2: 30 points
  - Step 3: 40 points
  - Intuitiveness and Design of the UI: 30 points extra credit
  - TODO: extra credit for advanced use of materials/lighting effects
