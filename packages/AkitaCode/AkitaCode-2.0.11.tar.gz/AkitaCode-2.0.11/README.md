# AkitaCode Python Library

You can consult the documentation for this library in the [Wiki page of the official GitHub repository](https://github.com/alexamatausa/akitacode "AkitaCode GitHub repository").

## History log

### Version 2.0.10

- Fixed an issue when import a Variable or Argument to an existing Frame in a same Situation Instance. This caused the same frame to be sent X times, where X is the number of variables or arguments contained in the CAN frame.

### Version 2.0.9

- Fixed ``State`` initzalitzation in module ``line_state_machine.py``.

### Version 2.0.8

- Fixed a bug during database export.

- Improved code readability and style.

### Version 2.0.7

- Fixed the problem with enviroments vector constants during method ``make()`` AKITA Testbench Document.

- Fixed the classification problem during automatic vectorization of environments and situations.

### Version 2.0.6

- The ``dict()`` method is added to the ``Information`` class to facilitate the handling of ARP files.

- ``Vector`` types have been declared as constants to improve code handling, scalability, and readability.

- The way the names of environments and situations are generated has been changed, correcting a security issue.

- Improved code readability and style.

### Version 2.0.5

- Fixed the error during the generation of the AKITA file. No data was imported into the protocol datablock. The protocol datablock was not blocked.

- The automatic capitalization rule is disabled when adding or modifying protocols, variables, functions, and arguments.

### Version 2.0.4

- Solved dependences of ``Messages`` module.

### Version 2.0.3

- The ``Messages`` module is added to the library that allows better management of messages sent and received between threads.

- Current implementations remain backward compatible with previous versions, since the ``Message`` superclass has a STR method.

- Status messages are added to the methods of the ``Document`` class.

- The `make()` method is added, which allows all methods of the ``Document`` class to be executed. To ensure proper compilation, we highly recommend using this method.

### Version 2.0.2

- Fixed an issue during the call to a *for* instance, where the evaluated variables were not correctly set as environment constants.

- Deleted some debug print to stdout.

- The conditions for the correct evaluation of arguments dependent on the specified environment when using a *for* instance are modified.

- Fixed an indexing error during export of functions and arguments.

- Support is added for the use of functions within "for" instances, allowing environment constants to be set as the value of the arguments.

### Version 2.0.2-beta

- Fixed problem during *for* line statement. Now, *for* statements can be used as following:

```
for each case of ( BAT_Temperature , BAT_SOH , BAT_SOC ) do
```

### Version 2.0.1

- Library dependencies have been fixed.

### Version 2.0.0

- First version.