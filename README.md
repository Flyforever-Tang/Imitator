# imitator
Monitor the operation of mouse and keyboard and repeat it. The operation sequence can be saved and loaded.

This is a tool that can help you save time for repeated operations, such as repeated copying, pasting and turning pages, which may help you simulate manual operations on some web pages that can't directly use crawlers to crawl data.

## Operation interface
![1](https://user-images.githubusercontent.com/54651776/157024463-8b946e6b-f1bc-4a32-870f-d7ec3e253d28.png)


## Instructions
- **Repeat Times**(*InputText*)

How many times you would like to repeat. If you enter any number **less than 0**, the program will repeat **sys.maxsize** times. Default value is **-1**(repeat **sys.maxsize** times).

- **Repeat Interval**(*InputText*)

Repeat interval(**unit: second**) of each step in event list. It is **not recommended to set it as a too small value**, in especial 0. Otherwise, the operations may can not be correctly detected by the system. Default value is **0.1**.


- **Round Interval**(*InputText*)

Repeat interval(**unit: second**) between repetitions. Default value is **0.1**.

- **Ignore Mouse Repeat**(*Radio*)

Whether ignore repeated mouse move events. If select **Ture**, the monitor while only record the destination, rather than the complete moving path of your mouse. Default value is **True**


> For example, if your mouse move from ***(1045, 463)*** to ***(1071, 465)***, the event list is as below:
> 
> > Ignore Mouse Repeat: **True**
> 
> > > [Mouse move to (1071, 465)]
> 
> > Ignore Mouse Repeat: **False**
> >
> > > [Mouse move to (1045, 463), Mouse move to (1046, 463), Mouse move to (1048, 463), Mouse move to (1050, 463), Mouse move to (1051, 463), Mouse move to (1053, 464), Mouse move to (1055, 464), Mouse move to (1057, 464), Mouse move to (1057, 464), Mouse move to (1059, 464), Mouse move to (1060, 464), Mouse move to (1061, 464), Mouse move to (1062, 464), Mouse move to (1064, 464), Mouse move to (1066, 465), Mouse move to (1066, 465), Mouse move to (1068, 465), Mouse move to (1069, 465), Mouse move to (1070, 465), Mouse move to (1071, 465)]

I strongly recommend setting **Repeat Interval** to a smaller value(such as **0.001**) if you set this option **False**, or the program may behave intermittently.

- **Ignore Keyboard Repeat**(*Radio*)

Whether ignore repeated keyboard events. This is used to solve the problem that when a key is pressed and held for a moment, the monitor will repeatedly listen to the same keyboard press event. Default value is **True**.

> For example, if your press **S** and hold, the event list is as below:
> 
> > Ignore Keyboard Repeat: **True**
> 
> > > [Keyboard press 's', Keyboard release 's']
> 
> > Ignore Keyboard Repeat: **False**
> >
> > > [Keyboard press 's', Keyboard press 's', Keyboard press 's', Keyboard press 's',..., Keyboard press 's', Keyboard release 's']

- **Start Listening**(*Button*)

Start listening and recording your operations. 

- **Stop Listening**(*Button*)

Stop listening and recording your operations. If you use IDE to run this program, the recorded event list will be printed. 
> **Attention!** The operation of **clicking this button** will not be recorded, as the program will pop the last 2 operations(*Mouse press Button.left, Mouse release Button.left*) from the list.


- **Repeat**(*Button*)

Start repeating your operations. It you want to stop repeating anytime, just **shake your mouse** so that the program can detect an unexpected mouse move event and stop.

- **Save Operations**(*Button*)

Save operations to the disk so that you can use it the next time you open this program. 
> There is a bug that this program can not save operations that contain **keyboard event**, and will riase error "**can't pickle \_thread.RLock objects**". This may be caused by thread lock and I do not know how to fix it. If you have any advise, please leave a message and thanks for your help!


- **Load Operations**(*Button*)

Load operations from the disk.

## Future work and possible updates

1. Figure out how to save keyboard operations.
2. Add an interface that can display and edit the event list, so as to screen out unnecessary operations.



# **Hope to be useful, and if you have any suggestions or problems, please leave a message. :)** #
