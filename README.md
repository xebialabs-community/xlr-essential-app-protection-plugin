## Build Status

[![Build Status][xlr-arxan-plugin-travis-image]][xlr-arxan-plugin-travis-url]
[![Codacy](https://api.codacy.com/project/badge/Grade/71d5adb3b2634edc875bd8c73cc3f24b)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-arxan-plugin&amp;utm_campaign=Badge_Grade)
[![License: MIT][xlr-arxan-plugin-license-image]][xlr-arxan-plugin-license-url]

## Preface

This Plugin offers an interface between Release and Essential Application Protection.

## Building the plugin

`./gradlew clean build`

## Testing the plugin

Run the following command to run a local docker container with the plugin installed.  

`./gradlew runDockerCompose`

Per the configuration at `src/test/resources/docker/docker-compose.yml,` the ports are defined so you can browse the local instance at:

`http://localhost:35516` 

## Overview

### Features

#### Server Configuration

Add a sever configuration in the Release Shared Configuration page for each server or login you wish to manage.

Each entry has the following configuration items in its definition:

##### Basics
*   Title - the name by which you will be referring to this definition in your Release Tasks.
*   Base URL - base URL of the Arxan Developer Portal API (https://api.developer.arxan.com).

##### Authentication
*   Portal Key (obtained from Developer Portal).
*   Portal Secret (obtained from Developer Portal).
*   License Token (obtained from Developer Portal).
*   AppAware Application Token (found on Developer Portal).
*   AppAware Application Endpoint (found on Developer Portal, currently is https://tps.touchstatistics.com).

The Tasks are based on the [Essential Application Protection API Docs](https://developer.arxan.com/doc/content/protect-essential/index.htm#t=Protect_Using_the_API.htm).

#### Get Authentication Token
Use this task to obtain an Authentication Token based on your credentials (Portal Key and Portal Secret).

##### Input Parameters
- Server. As configured in Release configuration.

##### Output Parameters
* Authentication Token.

#### Upload APK
Upload the APK to the Essential Application Protection cloud.

##### Input Parameters
- Server. As configured in Release configuration.
- Auth String. Authentication string `Bearer ${authToken}`.
- File. Local path to the APK file to upload.

##### Output Parameters
- Protection ID. If successfully uploaded, Essential Application Protection provides a `${protectionID}`.

#### Get Status
Get the status of protection.

##### Input parameters
- Server. As configured in Release configuration.
- Auth String. Authentication string `Bearer ${authToken}`.
- Protection ID. From previous step, `${protectionID}`.

##### Output Properties
- Protection Status. `done` if done.

#### Download Protected APK
Download the protected APK file.

##### Input Parameters
- Server. As configured in Release configuration.
- Auth String. Authentication string `Bearer ${authToken}`.
- Protection ID. From previous step, `${protectionID}`.
- Protected File Download Path. Local path to the folder to which to download the protected APK file.

##### Output
- If successful, you should now see the file downloaded to your specified local folder.

#### Delete APK from Server

Delete the uploaded APK file from the Essential Application Protection cloud.

##### Input parameters
- Server. As configured in Release configuration.
- Auth String. Authentication string `Bearer ${authToken}`.
- Protection ID. From previous step, `${protectionID}`.

##### Output Properties
- Status. `200` means success.

[xlr-arxan-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-arxan-plugin.svg?branch=master
[xlr-arxan-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-arxan-plugin
[xlr-arxan-plugin-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xlr-arxan-plugin/badges/gpa.svg
[xlr-arxan-plugin-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xlr-arxan-plugin
[xlr-arxan-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-arxan-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-arxan-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-arxan-plugin/total.svg
