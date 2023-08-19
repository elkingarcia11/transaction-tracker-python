# Transaction Tracker (Python & NoSQL)

The Transaction Tracker is a Python project designed to facilitate transaction management within a MongoDB or Cloud Firestore database.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Prerequisites](#prerequisites)
4. [Usage](#usage)
5. [Features](#features)
6. [Screenshot](#screenshots)
7. [Contact Information](#contact-information)
8. [Acknowledgments](#acknowledgments)
8. [Roadmap](#roadmap)

## Installation
To set up and install the project, follow these steps:

- Install the `pymongo` library using the following command:
`pip install pymongo`
- Install the `bson` library using the following command:
`pip install bson1
- Install the `firebase-admin` library using the following command:
`pip install --upgrade firebase-admin`

## Configuration

- Create and configure the `.ini` file with the local database connection details.
- Create and configure the `keys/credentials.json` file with Cloud Firestore database connection details.

## Prerequisites

Before running the project, ensure you have the following prerequisites:

- [ ] `pymongo` installed
- [ ] `bson` installed
- [ ] `.ini` file created & configured
- [ ]  `keys/credentials.json` file created & configured

## Usage

### Development

1. Execute the command `python3 main.py` in the command line to launch the Transaction Tracker.
2. Utilize key inputs to access various program features:
   - Enter `G` to retrieve transactions.
   - Enter `A` to add transactions.
   - Enter `U` to update transactions. 
   - Enter `D` to delete transactions.
4. Follow the on-screen instructions to execute the desired commands.

## Features

- Simplified transaction management from the command line: Easily add, update, delete, and retrieve transactions within a MongoDB or Cloud Firestore database.
- Duplication prevention: Interact with the MongoDB or Cloud Firestore database to prevent redundant transactions.
- Efficient tracking: Effectively monitor and manage posted transactions for enhanced financial management.

### Screenshot

![Program Snippet](./image.png)

## Contact Information

For inquiries, feedback, or questions, don't hesitate to contact me via email at elkingarcia.11@gmail.com or connect with me on [LinkedIn](https://www.linkedin.com/in/elkingarcia11/).

## Acknowledgments

This project makes use of [PyMongo](https://pymongo.readthedocs.io/) and [Firebase Admin Python SDK](https://firebase.google.com/docs/reference/admin/python), Python libraries containing tools for working with MongoDB and Cloud Firestore.

## Roadmap

The success of the Transaction Tracker project laid the foundation for the Transaction Tracker API program. This program enables our operations team to monitor the company's financial activities using their mobile devices.
