# Socket-Programming

## IMPLEMENTATION of QUIZ using SOCKET PROGRAMMING...

## INTRODUCTION:
This is a socket quiz implemented using PYTHON3. This is a simple implementation of a game show. Here, there is a host who conducts the show and others are players who provides the answers.

## ASSUMPTIONS:
1. There has to be exactly 3 clients (or players) so as to begin with the quiz.
1. The question is chosen randomly from a set of 20 questions.
1. Awarded +1 for a correct answer and -0.5 for an incorrect answer
1. It is declared a TIE if none of the players are able to score atleast 5 points or if the question set is over.
1. The player who scores atleast 5 points first is declared as the winner.

## INSTRUCTIONS TO RUN:
1. Download the server.py and the client.py as each of them is the code for the server side and the client side respectively.
1. Run the following command on the terminal after going into the directory in which the two files are present:<br />
`python3 server.py <your IP address> <Port number>`
1. Open three terminals (each as a player) and type the command as:<br />
`python3 client.py <your IP address> <Server’s Port number>`<br />
(This could be done on multiple systems instead on a single desktop)
  
## PROJECT BRIEF:
The quiz needs to have three players so as to begin. The host (server) has a set of 20 questions which will be asked one by one (without repetition) to all the players. The question is chosen randomly and sent to all the players. Then, the players need to press any key on the keyboard as the buzzer. The first one who presses the buzzer is given the chance to answer the question. If the question is answered correctly +1 is awarded or else negative points (0.5) is deducted. Then the host proceeds with the next question until one of the players scores atleast 5 points or the question set is over.
