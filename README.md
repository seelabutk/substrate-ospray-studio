# Project Description

In this project, the goal is to set up a cloud-based rendering service using Amazon AWS. In other words, Rendering as a Service (RaaS). You will use concepts and tools that were first proposed and tested out through Visualization as a Service (VaaS) research that started around 2015 at the University of Tennessee, Knoxville with funding from NSF and Intel. 

Specifically, you will use Substrate, which is our latest effort to consolidate the tools needed to create a VaaS or a RaaS. The back-end rendering engine you will use is OSPRay. Both Substrate and OSPRay are open source:
     Github link 1: https://github.com/seelabutk/substrate
     Github link 2: https://github.com/ospray/ospray

After setting up the RaaS, your next tasks are to build a scene, build a front-end UI in a web browser using Javascript so that you can interact with the scene, and then create a movie by setting and controlling key frames. The specific requirements are as follows.

Step 1. Set up a RaaS

1a. Set up your own AWS account. Go to ____, follow instructions on ____

1b. Download xxx

1c. Run commands yyyy (use only AWS Tiny instances to start).

1d. The method to communicate with RaaS is through a very restrictive API. All you get to do is to send a rendering request. For this substrate:ospray RaaS, your rendering request looks like the following. ….

A default one is provided to you. Here is some basic information. You can ping your substrate:ospray RaaS through the following curl command.
 
   ….

Step 2. Build a browser UI to control the RaaS. Your UI must allow: (a) placing an object into the scene, (b) set up a light source, and (c) set up camera positions. 

You will do so using JQuery …



Step 3. Add functionality in your browser UI to record keyframes and submit to the substrate:ospray RaaS to render the movie

Grading points.

      Step 1: 20 points
      Step 2: 20 points
      Step 3: 20 points
      Complexity of the scene. Your scene must have no less than 3 objects. Effects should include xxxx: 40 points
      Intuitiveness and Design of the UI: 15 points extra credit
