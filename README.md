# MPSoCBench_IC_2019

![MPSOCBENCH](https://github.com/IsabelleFSNunes/MPSoCBench_IC_2019/blob/master/image/logoMpsocbench.png)

You must put the mpsocbench.py and folder image on the same directory of MPSoCBench.

## Some version of Python needs install:

### Tkinter
```
~/MPSoCBench/$ sudo apt-get install python-tk python3-tk
```
PIL and imagetk 
```
~/MPSoCBench/$ sudo apt-get install python-pil

~/MPSoCBench/$ sudo apt-get upgrade python3-pil.imagetk
```


The command in the terminal for use the GUI mpsocbench:

```sh
~/MPSoCBench/$ source env.sh
```
```sh
~/MPSoCBench/$ python3 mpsocbench.py
```
## CSV - Updates : 
---

You must need add in the file define.h

**Path reference**
```
~/Documents/MPSoCBench/defines.h
```
add this line :
```c
#define LOCAL_FILE_MEASURES_NAME_CSV "local_report.csv"
```

---
* <h2>Times local-report:</h2>

1. **Path reference**:
```
~[Documents]/archc/src/aclib/ac_utils/
```
 to update with the file's Path on git: : 
```
~/MPSoCBench_IC_2019/Others/1/archc.cpp 
```
---
2. **Path reference**:
```
~[Documents]/archc/src/aclib/ac_core/
```
 to update with the file's Path on git: : 
```
~/MPSoCBench_IC_2019/Others/2/ac_arch.H
```
----

3. **Path reference**:
```
~[Documents]/archc/include/
```
 to update with the file's Path on git: : 
```
~/MPSoCBench_IC_2019/Others/3/ac_arch.H
```
---
4. **Path reference**:
```
~[Documents]/mpsocbench/platforms/platform.router.lt/
```
to update with the file's Path on git: 
```
~/MPSoCBench_IC_2019/Others/4/main.cpp
```
---
5. **Path reference**:
```
~[Documents]/mpsocbench/platforms/platform.noc.lt/
```
to update with the file's Path on git: 
```
~/MPSoCBench_IC_2019/Others/5/main.cpp
```
----
6. **Path reference**:
```
~[Documents]/mpsocbench/platforms/platform.noc.at/
```
to update with the file's Path on git: 

```
~/MPSoCBench_IC_2019/Others/6/main.cpp
```
---
* <h2>Lock acess:</h2>
----
1. **Path reference**:
```
~[Documents]/mpsocbench/ip/tlm_lock/
```
to update with the file's Path on git: 
```
~/MPSoCBench_IC_2019/Others/7/main.cpp
```

---
* <h2>Router acess:</h2>

---
1. **Path reference**:
```
~[Documents]/mpsocbench/is/tlm_router/
```
to update with the file's Path on git: 
```
~/MPSoCBench_IC_2019/Others/8/main.cpp
```
---
2.  **Path reference**:
```
~[Documents]/mpsocbench/is/tlm_noc_at/
```
to update with the file's Path on git: 
```
~/MPSoCBench_IC_2019/Others/9/tlm_noc.cpp
```
---

- <h2>Memory acess:</h2>
---

1. **Path reference**:
```
~[Documents]/mpsocbench/ip/tlm_memory/
```
to update with the file's Path on git: 
```
~/MPSoCBench_IC_2019/Others/10/tlm_memory.cpp
```
---
2. **Path reference**:
```
~[Documents]/mpsocbench/ip/tlm_memory_at/
```
to update with the file's Path on git: 
```
~/MPSoCBench_IC_2019/Others/11/tlm_memory.cpp
```
---
 

