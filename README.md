# Project Description

In this project, your goal is to set up a cloud-based rendering service, or a Rendering as a Service (RaaS), using Amazon AWS running OSPRay Studio.
You will use concepts and tools that were first proposed and tested out through Visualization as a Service (VaaS) research that started around 2015 at the University of Tennessee, Knoxville with funding from NSF and Intel.

Specifically, you will use Substrate, which is our latest effort to consolidate the tools needed to create a VaaS or a RaaS. The back-end rendering engine you will use is OSPRay. Both Substrate and OSPRay Studio are open source:
  - Substrate: https://github.com/seelabutk/substrate
  - OSPRay Studio: https://github.com/ospray/ospray_studio

After setting up the RaaS, your next tasks are to build a scene, build a front-end UI in a web browser using Javascript so that you can interact with the scene, and then create a movie by setting and controlling key frames. The specific requirements are as follows.

# Project Steps

## Step 1 - Set up the RaaS

0. Clone this repository

    ```git clone https://github.com/seelabutk/substrate-ospray-studio```

1. Set up your own AWS account. Go to https://portal.aws.amazon.com/billing/signup and create a new account.

2. Follow [this guide](./docs/AWS_Account_Setup.md) to set up your CLI credentials.

3. Follow [this guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to install the AWS CLI.

4. Install [Node and NPM](https://nodejs.org/en/download/). Then run the following command to install the AWS CDK CLI:

    ```npm install aws-cdk@^1.147.0```

5. Install [Python 3.8 - 3.10](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/).

6. Install Substrate with `pip install seelabutk-substrate`.

7. Define the configuration for Substrate. This can be done by opening the file called `substrate.config.yaml` in your cloned repository. Set the `aws.bucket` property to `substrate-data-{YOUR_NETID}`.
For more information on the full options available to you, please see the (optional) [configuration API](https://github.com/seelabutk/substrate/blob/main/api/substrate.config.yaml).

8. Run the following command to deploy your RaaS to AWS - Make sure you run this command FROM the directory of your repo!

    ```substrate ospray_studio start```

9. The previous command should output a link where your RaaS can be accessed.

![ready](https://user-images.githubusercontent.com/8481770/163423219-494f3ecd-0727-4ac1-9f35-f6b15077be13.png)

Wait until your RaaS has had time to complete setup (this may take 10-15 minutes), then open the http version of this link (if your browser opens an https link, remove the s) and ensure that you can see the default OSPRay Studio scene display.
If your RaaS launched successfully, you should see a rendering of an apple after 6 seconds.

![apple](https://user-images.githubusercontent.com/8481770/163423252-2cdbdcdd-ee92-4d3d-8644-0b8420c45f70.png)

10. To kill your RaaS, run the following command:

    ```substrate ospray_studio stop```

The RaaS includes an API which can be used to submit rendering requests and get images or movies back. If the link outputted by your RaaS was http://127.0.0.1, then the following endpoints will be available to you:

    - http://127.0.0.1/ - This is the default endpoint that will serve a rendering of the objects specified in `substrate.config.yaml` to ensure the RaaS is available and working. You should open this endpoint in a browser after the RaaS has launched.
    - http://127.0.0.1/sg - Returns the SceneGraph that was used to perform the first rendering by the RaaS. This will not work until the previous endpoint has been opened in a browser.
    - http://127.0.0.1/render - Takes a SceneGraph as input and returns a PNG of the newly rendered frame. This should primarily be used to identify suitable SceneGraphs for use as key frames by the following endpoint.
    - http://127.0.0.1/renderMovie - Takes multiple SceneGraphs treated as key frames as input and returns a movie animating the scene through these key frames.

You can interact with these endpoints in a browser through the use of the Fetch API. Examples of how to use the Fetch API to communicate with each endpoint can be seen in the JavaScript file in the skeleton code for this project.
More details on the Fetch API can be found [here](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch). We have provided you with a raas.js file which contains basic functions which
implement this behavior for the above listed endpoints.

## Step 2 - Add your own objects to the scene

Start by going to [Poly Haven](https://polyhaven.com/models) and grabbing at least three objects to put in your scene instead of the apple. Make sure you download GLTF files to ensure compatibility with OSPRay Studio.
To ensure that you don't exceed the AWS free-tier limits for S3 and EFS, please make sure that you don't use more than 5GB of storage space.

Next, modify the `data.source` option in `substrate.config.yaml` to point to the directory containing these three files.

Now, repeat parts 8 & 9 of Step 1 to get a simple rendering with each of the objects in the scene. This will likely look poor or even chaotic, and you will next need to configure OSPRay Studio in order to improve it.

## Step 3 - Run the skeleton code

Before you can configure OSPRay Studio, you will need to begin using your own front-end to connect with the RaaS. We have provided skeleton code that replicates the behavior of the RaaS' front-end and provides examples of
interacting with the RaaS' API. This can be run with any static file server, even the one bundled with the version of Python you installed earlier. To use Python's server, run:

    python -m http.server 8080

Now, you can open http://localhost:8080 or http://127.0.0.1:8080 to view your front-end.

Before your front-end can show the rendering, you'll need modify the RAAS_LOCATION variable in `raas.js` to point to your RaaS. Then, reload your front-end and you should see the rendering of your objects.

Congragulations, at this point you have successfully interacted with every part of the system we have provided to you. The following steps asks you to create your own customizations to the system to enable quicker and easier interactions with the system.

## Step 4 - Use jsoneditor to modify the SceneGraph

OSPRay Studio is configured through what is referred to as a SceneGraph (.sg file). This is a JSON-formatted file that contains the information necessary to perform an OSPRay rendering.
You may retrieve the SceneGraph used to render the initial scene through the endpoint at {your_raas_link}/sg, or by calling the get_scene_graph function defined in raas.js.

Once you have the SceneGraph, changes can be made to the scene by editing the JSON and issuing a new rendering request to the RaaS. This can be done by calling re_render and passing your modified scene graph as a parameter to the function.

The scene graph is a large deeply nested JSON object. To get a feel for its structure and available values you can tweak, we suggest you implement some sort of editor in which you can modify the JSON and make new ScenGraph objects with. 

We have included [JSON Editor](https://github.com/josdejong/jsoneditor) in the skeleton code for this project. Here is an example of how it could look once incorporated into your UI.

![jsoneditor](https://user-images.githubusercontent.com/8481770/163428586-d2b99832-2a15-4732-879a-17ed52ab85be.png)

This Scene Graph editor is ultimately not required to be implemented in this project, but may be a useful starting point. By providing only a JSON editor, users will have to be very familiar with where important attributes are located within the Scene Graph to be capable of using your system. Every attribute of the scene graph is not required to be modified, so you can create a UI which is responsible for editing only a subset of the scenegraph which you deem important, further reducing the need for a fully-fledged JSON editor. You should focus on making your UI clean and intutive. 

To use the edited SceneGraph to produce a new rendering, send a POST request to {your_raas_link}/render that contains your new SceneGraph in the request body. This can be done through calling the re_render function in raas.js, passing your scene graph as a parameter.
The response from the server, if your SceneGraph is valid, will be a PNG-formatted image with the newly-rendered frame.

Ultimately, to complete this step, complete freedom is given to you to implement whatever UI you would like in order to accomplish modifying/creating a SceneGraph Object. You may choose to create one from scratch, or modify the existing SceneGraph in memory. You may create a Node Project, use npm packages, or libraries and tools you find online. The only requirement is that the final submission to your git repo be runnable without a build step - If your project requires a build step then you can build your project yourself and put it in a /dist directory if necessary.

## Step 5 - Add functionality to your browser UI to create movies

The RaaS also supports the creation of movies. To do so, you may save multiple SceneGraphs with different parameters (such as the camera position) as key frames, and then send them via a POST request to {your_raas_link}/renderMovie.
The RaaS will perform a linear interpolation between each key frame and produce an AV1-encoded .mp4 file with the request length and frame rate. The format of the body of your POST request should look as follows:

    {
      frames: Array of SceneGraphs to use as key frames,
      fps: your desired fps,
      length: your desired video length in seconds
    }

This process may be slow due to the need to render large numbers of frames, so consider beginning with something small such as a 2-second, 10-fps video. Also, please note that the video may not exactly match your desired length and frame rate after being encoded.

Alter your Step 4 UI to also support (a minimum of) the creation and modification of keyframes and a render movie button.

# Grading criteria

  - Step 1: 10 points
  - Step 2: 10 points
  - Step 3: 10 points

  - Step 4: 50 points
    - Intuitiveness and design of the UI: up to 15 points extra credit

  - Step 5: 50 points
    - Intuitiveness and design of the UI: up to 15 points extra credit
  
  - A Scene rendered along with the scenegraph and objects required to render it: 10 points
    - Use of material, lighting effects, objects, and design: up to 10 points extra credit

  - A Movie rendered along with the scenegraph and objects required to render it: 10 points
    - Use of material, lighting effects, objects, and design: up to 10 points extra credit

Total: 150 points

Total with all Extra Credit: 200/150 = 133%
