# circular-exchange-algorithm

The aim of this algorithm is to go beyond the classical one to one exchange in a barter system and overcome
the "double coincidence of wants" as it is difficult to find someone who has what you want and is willing to trade for what you have. This limitation led to the development of money, which allows for more efficient exchange and trade.

## Double coincidence of wants
Example:
* Bob has a computer and wants to exchange it for a bicycle.
* Henri has a bicycle and wants to exchange it for a computer.

Resolution: there is a double coincidence of wants, Bob and Henri both have what the other wants.
* Bob gives the computer to Henri
* Henri gives the bicycle to Bob

## Circular exchange
Example:
* Bob has a computer and wants to exchange it for a bicycle.
* Henri has a bicycle and wants to exchange it for a piano.
* Adele offers French lessons and wants to exchange it for a computer.
* Zoe has a piano and wants a French lesson.

Resolution: there is no double coincidence of wants, but there is a possibility for a circular exchange!
* Bob gives the computer to Adele
* Henri gives the bicycle to Bob
* Adele gives the French lessons to Zoe
* Zoe gives the piano to Henri

## Value of the traded items
Each item that is made available to the system must have a value in order to make acceptable trades for every user.


## Additional ideas
* Recommendation algorithm for the users based on the available items in order to trigger an exchange
* Possibility to change the algorithm behaviour via a configuration file

# Technical informations

## Code quality
To ensure the consistency and quality of the code, here are the tools that are being used
- [pre-commit](https://pre-commit.com/) that executes multiple code validation tools when a commit is done (see [its configuration](https://github.com/Sean-OShea/circular-exchange-algorithm/blob/main/.pre-commit-config.yaml))
- [flake8 to validate the python code](https://flake8.pycqa.org/en/latest/)
- [black for autoformatting the python code](https://github.com/psf/black)
- [isort to handle imports ordering in python](https://github.com/PyCQA/isort)
