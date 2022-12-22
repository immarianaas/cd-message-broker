<div id="readme-top"></div>


<!-- PROJECT SHIELDS -->
<div align="center">

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!--
[![Contributors][miguel-github-shield1]][miguel-github-url]
[![Contributors][mariana-github-shield1]][mariana-github-url]
<strong><< Mariana | Miguel >></strong>

[![LinkedIn][mariana-linkedin-shield1]][mariana-linkedin-url]
[![LinkedIn][miguel-linkedin-shield1]][miguel-linkedin-url]
-->

[![LinkedIn][mariana-linkedin-shield1]][mariana-linkedin-url]
[![Contributors][mariana-github-shield]][mariana-github-url]
<strong>☜(⌒ᵕ⌒)☞</strong>
[![Contributors][miguel-github-shield]][miguel-github-url]
<!--
[![LinkedIn][miguel-linkedin-shield1]][miguel-linkedin-url]
-->


<!--
☜(⌒▽⌒)☞
<strong>☜(⌒▽⌒)☞</strong>
<strong>☜(⌒ᵕ⌒)☞</strong>
<strong>☜( ˊᵕˋ )☞</strong>
ଘ(੭*ˊᵕˋ)੭* ̀ˋ 
-->
</div>


<!-- PROJECT LOGO 
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
  -->

<div align="center">


<h3 align="center">Message Broker</h3>

  <p align="center">
    The first project of the <a href="https://www.ua.pt/en/uc/12273">Distributed Computation</a> course, lectured at University of Aveiro, in the academic year of 2019/2020, as part of my BSc in Informatics Engineering. Project done with Miguel Almeida.

  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#introduction">Introduction</a></li>
    <li><a href="#whats_done">What's done</a></li>
    <li><a href="#whats_to_improve">What's to improve</a></li>
    <li><a href="#try_it_on_your_machine">Try it on your machine</a></li>
    <li><a href="#files_overview">Files Overview</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
<!-- ## About The Project -->

<h2 id="introduction">Introduction</h2>
A <strong>message broker</strong> is a type of middleware typically used in distributed systems which need EAI (Enterprise Architecture Integration). Many companies are provided with different kinds of software which need to be integrated to achieve the business logic desired. Message brokers come into play to translate the communication between the different processes, allowing the integration of different software even if they have distinct protocols and data serialization methods.

### Goals
The goal of this work was to develop a message broker able to connect `producers` and `consumers` through a Pub/Sub protocol and three distring serialization mechanisms: `XML`, `JSON` and `pickle`. This protocol also needed to be designed and implemented over TCP. Furthermore, the message broker should be able to retain messages, so that when a `consumer` subscribes to a topic, it receives the last message post there.

<strong>Note</strong>: the information presented on both <strong>Information</strong> and <strong>Goals</strong> are described with more detail in the project guide, which is in Portuguese.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<h2 id="whats_done">What's done</h2>
The message broker we developed fulfills every goal and requirement mentioned above, operating with `raw sockets` and `selectors`.
Additionally, the broker implements the notion of hierarchical topics: if a `consumer` subscribes to a topic, it is also automatically subscribed to all the its "children" topics. This was acomplished with the implementation of a tree structure.
This broker is also prepared to handle multiple connections at the same time, be it `producers` or `consumers`, and they can join or leave the system at any time without problem.

### Protocol
#### Connection procedure
Any process can connect to the broker by sending a message with 1 byte, to inform the serialization type it will use to communicate. 
| message value | serialization type |
| ------------- | ------------------ |
| 1             | `JSON`               |
| 2             | `XML`                |
| 3             | `pickle`             |

The broker will then save this information so that it will be able to decode every message sent by that process.

#### Messages' structure
Every message needs to contain information on its size, so that it can be read correctly. For this, we defined that the first 5 bytes of any message are reserved for its length. The only exception is the message mentioned above, since it can only be 1 byte.

There are 4 messages that will be accepted by the broker (in the 3 different serialization types):
| operation   | message format (represented in JSON) |
| ----------- | ------------------------------------------------------------ |
| join/subscribe topic | `{'OP': 'join', 'TOPIC': <topic(str)>, 'TYPE': <type(int)>}` |
| publish | `{'OP': 'publish', 'VALUE': <value(str)>}`                   |
| list topics | `{'OP': 'topics_request'}`                                   |
| leave topic | `{'OP' : 'leave_topic'}`                                     |


The types are mapped as follows:
| type value | type    |
| ---------- | -------- |
| 1          | `CONSUMER` |
| 2          | `PRODUCER` |

The topics (represented with `<topic(str)>` in the table) follow the common hierarchical directory representation `/parent_topic/child_topic/...`.

To finish, this next table shows the format of the messages sent by the broker (also in the 3 different serialization types):
| function | message format (represented in JSON) |
| ---------- | -------- |
| list existing topics | `{'OP' : 'topics_list', 'LIST' : <topic_list(str)>}` |
| send published message | `{'TOPIC': <topic(str)>, 'VALUE': value}` |

Here, the topic list (represented with `topic_list(str)`) is a string with each existent type separated by the `\n` character. For example, `'temp\nmsg'` represents two topics: `temp` and `msg`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<h2 id="whats_to_improve">What's to improve</h2>
Even though the goals for this project were achieved and even exceeded, there are quite a lot of things that could be improved. 

To start, the code can sometimes be confusing and not intuitive, with some blocks unecessarily replicated. The documentation could also be improved, not to mention the mix of Portuguese and English when naming variables.

<!--
Even though the goals were achieved successfully, there are quite a things that I notice could use some improvement, looking back after some years. For one, the code could be better organized and documented. The mix of Portuguese with English shouldn't be there.
-->

Even though this is a bit outside the scope of the project, there are some clear improvements to the protocol that should be considered. For example, it should be possible for `publishers` to publish in many topics, selecting which one(s) in every publish message. The `consumer` should also be able to leave a specific topic, instead of being forced to unsubscribe of all of them. 

The current code to simulate the `consumers` and `producers` is quite limited, as we weren't supposed to edit these files for submittion. These processes should be improved in order to accomodate for all the functionalities of the message broker. Furthermore, some properties, such as the server port, could be defined with command-line arguments.

<!--
Apart from that, there are some clear improvements to the protocol. Since this Message Broker was created for a specific `consumer` and `producer` provided by the professors, it was important to follow their requirements. For a general setting, it would make sense change the protocol. For example, it should be possible for publishers to publish in many topics, selecting each one in every publication. Besides, the consumer should also be able to leave a specific topic, instead of all the topics it is subscribed to.
-->
It would also be interesting to introduce unit and integration tests to the project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
<h2 id="try_it_on_your_machine">Try it on your machine</h2>

Below are described the steps to test the system.

### Prerequisites & Setup

You should have at least Python 3.8 installed on your machine. You can find out how <a href="https://www.python.org/downloads/">in the official page</a>.

Then you just need to clone the repository:
```bash
git clone https://github.com/immarianaas/cd-message-broker.git
```

### Usage

#### Message broker
To activate the message broker, you just need to execute `broker.py`:
```bash
python3 broker.py
```
By default, port 8000 will be used. Currently it is not possible to select which port to use dynamically.

#### Consumer process
To run the example `consumer` process, you need to execute `consumer.py`, which will connect to the broker on port 8000. We can provide it with an argument to select which topic it is going to join:

| optional argument | description                           | default |
| ------------------ | -------------------------------------- | ------- |
| `--type`           | type of producer: [`temp`, `msg`, `weather`] | `temp`    |

If the argument isn't one of the allowed values, an error will be shown and the process stoped.

##### Example
```bash
python3 consumer.py --type msg
```

#### Producer process
To run the example `producer` process, you need to execute `producer.py`, which will also connect to the broker on port 8000. We can provide it two arguments to select both the topic and the number of messages that will be sent:

| optional argument | description  | default |
| ---------- | -------------------------------------- | -------- |
| `--type`   | type of producer: [`temp`, `msg`, `weather`] | `temp`     |
| `--length` | number of messages to be sent          | 10       |

##### Example
```bash
python3 producer.py --type msg --length 5
```

<br />
<strong>Note:</strong> just want to highlight that these last two files did not suffer a lot of changes from the base code provided to the students, since they were not part of the assignment.
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
<h2 id="files_overview">Files Overview</h2>
<!-- 
The branch <a href="https://github.com/immarianaas/cd-message-broker/tree/original">`original`</a> is where an unaltered version of the project will be placed. If one day this code is to be improved, that branch will remain the same.
-->

| file                         | description                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------- |
| `Relatorio1.pdf` | Report of the project where the code and protocol is explained, in Portuguese |
| `Projecto 1 - CD2020.pdf` | Project guide provided by the professors, also in Portuguese |
| `broker.py` | Core functionality for the message broker |
| `topicos.py` | Topic tree implementation |
| `tree.py`| Alternative topic tree implementation |
| `consumer.py` | Consumer logic for testing purposes |
| `producer.py` | Producer logic for testing purposes |
| `middleware.py` | Common functionality for sending and receiving messages, as well as the marshalling process |
| `utils.py` | Helper function to handle XML data |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
<h2 id="license">License</h2>

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
<h2 id="acknowledgments">Acknowledgments</h2>

[DETI - Departamento de Eletrónica, Telecomunicações e Informática](https://www.ua.pt/pt/deti)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[forks-shield]: https://img.shields.io/github/forks/immarianaas/cd-message-broker.svg?style=for-the-badge
[forks-url]: https://github.com/immarianaas/cd-message-broker/network/members

[stars-shield]: https://img.shields.io/github/stars/immarianaas/cd-message-broker.svg?style=for-the-badge
[stars-url]: https://github.com/immarianaas/cd-message-broker/stargazers

[issues-shield]: https://img.shields.io/github/issues/immarianaas/cd-message-broker.svg?style=for-the-badge
[issues-url]: https://github.com/immarianaas/cd-message-broker/issues

[license-shield]: https://img.shields.io/github/license/immarianaas/cd-message-broker.svg?style=for-the-badge
[license-url]: https://github.com/immarianaas/cd-message-broker/blob/master/LICENSE

<!--
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
-->

[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 





[mariana-github-shield1]: https://img.shields.io/badge/--black.svg?style=for-the-badge&logo=github&colorB=555
[mariana-linkedin-shield1]: https://img.shields.io/badge/--black.svg?style=for-the-badge&logo=linkedin&colorB=0e76a8

[mariana-github-shield]: https://img.shields.io/badge/-Mariana-black.svg?style=for-the-badge&logo=github&colorB=555
[mariana-linkedin-shield]: https://img.shields.io/badge/-Mariana-black.svg?style=for-the-badge&logo=linkedin&colorB=555

[mariana-github-url]: https://github.com/immarianaas
[mariana-linkedin-url]: https://www.linkedin.com/in/immarianaas



[miguel-github-shield1]: https://img.shields.io/badge/--black.svg?style=for-the-badge&logo=github&colorB=555
[miguel-linkedin-shield1]: https://img.shields.io/badge/--black.svg?style=for-the-badge&logo=linkedin&colorB=0e76a8

[miguel-github-shield]: https://img.shields.io/badge/-Miguel-black.svg?style=for-the-badge&logo=github&colorB=555
[miguel-linkedin-shield]: https://img.shields.io/badge/-Miguel-black.svg?style=for-the-badge&logo=linkedin&colorB=555

[miguel-github-url]: https://github.com/Miguel17297
[miguel-linkedin-url]: https://github.com/immarianaas/cd-message-broker

[Python-logo]: https://img.shields.io/badge/Python-306998?style=for-the-badge&amp;logo=python&amp;logoColor=white
[Python-url]: https://python.org