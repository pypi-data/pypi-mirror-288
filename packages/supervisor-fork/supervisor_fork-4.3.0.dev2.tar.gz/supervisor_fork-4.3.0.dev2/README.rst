Supervisor-fork
===============

This project is a fork of the [Supervisor](https://github.com/Supervisor/supervisor) project.
The original project is licensed under the following terms:
https://github.com/Supervisor/supervisor/blob/main/LICENSES.txt


What's New
----------


Add init_py config in supervisord to do init job
------------------------------------------------

.. code-block:: conf

  [supervisord]
  init_py=%(here)s/init_supervisord.py

- import the py file and call the main(logger_obj) function
  

Fork to create subprocess, not only execve
------------------------------------------
.. code-block:: conf

  [program:app1]
  command=%(here)s/my_app2.py arg1 arg2
  is_module=true

- command must reference to a python script, arg is optional
- is_module=true：not use execve to start the command, but use fork in supervisord, and call the main(arg1, arg2, ...) in the py

.. note::
  not config init_py and is_module, you use it as the original supervisor


Contributing
------------

We'll review contributions from the community in
`pull requests <https://help.github.com/articles/using-pull-requests>`_
on GitHub.
