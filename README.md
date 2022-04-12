# Project Description

In this project, your goal is to set up a cloud-based rendering service, or a Rendering as a Service (RaaS), using Amazon AWS running OSPRay Studio.
You will use concepts and tools that were first proposed and tested out through Visualization as a Service (VaaS) research that started around 2015 at the University of Tennessee, Knoxville with funding from NSF and Intel.

Specifically, you will use Substrate, which is our latest effort to consolidate the tools needed to create a VaaS or a RaaS. The back-end rendering engine you will use is OSPRay. Both Substrate and OSPRay Studio are open source:
  - Substrate: https://github.com/seelabutk/substrate
  - OSPRay Studio: https://github.com/ospray/ospray_studio

After setting up the RaaS, your next tasks are to build a scene, build a front-end UI in a web browser using Javascript so that you can interact with the scene, and then create a movie by setting and controlling key frames. The specific requirements are as follows.

### Step 1 - Set up the RaaS

1. Set up your own AWS account. Go to https://aws.amazon.com/ and create a new free-tier account.

2. Follow [this guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/howtogetcredentials.html) to get your CLI credentials for AWS, and ensure they are available for the next steps.

3. Install [Python 3.8](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/).

4. Install Substrate with `pip install seelabutk-substrate`.

5. Define the configuration for Substrate. This can be done by creating a file called `substrate.config.yaml` in your working directory. The format and available options for this file can be found [here](https://github.com/seelabutk/substrate/blob/main/api/substrate.config.yaml). You will need to define the following:

  - data.source: a list of paths to the GLTF/OBJ files you want to load into your scene. Please ensure that the size of your objects doesn't exceed the free-tier limits.
  - aws.region: the AWS region you want to deploy to.
  - aws.managers: the list of EC2 instances you want to use to run your RaaS (a single instance should be sufficient for this project). Please ensure that your selected instance type is eligible for the free-tier.

6. Run the following command to deploy your RaaS to AWS:

  substrate ospray_studio start

7. The previous command should output a link where your RaaS can be accessed. Once your RaaS has had time to complete setup (this may take 10-15 minutes), open that link and ensure that you can see the default OSPRay Studio scene.
This should look very poor at this point, as your next goal will be to configure the scene to be well organized.

8. To kill your RaaS, run the following command:

  substrate ospray_studio stop

### Step 2 - Build a browser UI to control the RaaS. Your UI must allow: (a) placing an object into the scene, (b) set up a light source, and (c) set up camera positions.

### Step 3 - Add functionality in your browser UI to record keyframes and submit to the substrate:ospray RaaS to render the movie

### Grading criteria

  - Step 1: 20 points
  - Step 2: 20 points
  - Step 3: 20 points
  - Complexity of the scene. Your scene must have no less than 3 objects. Effects should include xxxx: 40 points
  - Intuitiveness and Design of the UI: 15 points extra credit
