# ModularJenkinsScripts
Organizations have several tasks the need to be automated. Eventually without a road map the automated scripts become unmanageable and developers will need to find a solution. Using the Template Pattern this project will allow users to develop independent automation scripts in python using a single interface. 

## Overview
There are several automated scripts that manage different procedures in Macromoltek. As the organization grows there will be more procedures to add. This document will explain what current scripts exist and how to add new scripts. 

# Requirements
Python3.6 or later

## How to Run

### Help 
  python Main.py help
  This will print out all avaliable modules and an example on running the code
  
### Example
  `python Main.py ModuleName arg1 arg2 argN`
  
## Adding Modules

Create a module from the ModuleTemplate.py
Write your code in the Run method and print out helpful information using the Help method

Once the code is finished store the Module in the `Tasks` folder then call:

`python Main.py ModuleName help`

This will validate your Module is called correctly
