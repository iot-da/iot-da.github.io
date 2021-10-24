# C programming. Exercises


There are many good C/C++ tutorials online. You can find one in [this link](https://www.cprogramming.com/tutorial/c-tutorial.html).

Next, there are several examples that we will use during the lectures to talk about different aspects of C language.

You can [download a ZIP with the examples here](C-Example.zip)

## Compilation (headers, macros...)
```c
#include <stdio.h>

/******** QUESTIONS/TASKS *****
* 1. Compile and execute the code
* 2. Later, apply only the preprocessor  (-E flag) and redirect the output
* to a file called hello.i
* 3. What happened to the call min()?
* 4. What did the directive  #include <stdio.h> produced?
*****************/
#define N 5

#define min(x,y) ( (x<y)?x:y )
int a = 7;
int b = 9;
int main() {

 char* cad = "Hello world";
 int i;

 for (i=0;i<N;i++) {
   printf("%s \t a= %d b= %d\n",cad,a,b);
   a++;
   a = min(a,b);			
 }
 return 0;
}
```

## Data types. Sizes

```c
#include <stdio.h>
/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 * 1. Why the first "printf" prints different values for the same variable 'a'?
 * 2. How large is a 'char' variable?
 * 3. Why the value of 'a' changes that much when adding 1?  
 * 4. If "long" and "double" have the same size, what's the difference?
 *****/
char a = 127;
int b = 41;
int main() {

	printf("a = %d a = %c \n", a,a);
	a++;
	printf("a = %d a = %c b=%d  b=%c\n", a,a,b,b);
	printf("Size of int: %lu\n",sizeof(int ) );
	printf("Size of char: %lu\n",sizeof( char) );
	printf("Size of float: %lu\n",sizeof(float ) );
	printf("Size of double: %lu\n",sizeof( double) );
	printf("Size of long: %lu\n",sizeof(long ) );
	printf("Size of short: %lu\n",sizeof( short) );
	printf("Size of void*: %lu\n",sizeof( void*) );

}
```

```c
#include <stdio.h>


/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 * 1. Is there a compilation problem or a execution problem?
 * 2. Why is it complaining? Fix it and compila again.
 * 3. a,b,c, y x are declared one after the other. Are their addresses consecutive in memory?
 * 4. What does the modifier "%lu" means in printf()? 
 * 5. Which address is "pc" pointed to? Is the address of any other variable? Are those two the same size?
 * 6. Does the size of "array1" matches the number of elements? Why?
 * 7. Do "cadena1" and "cadena2 "point to the same address? 
 * 8. Why sizes (according to sizeof()) of cadena1 and cadena2 are different?
 *************/

#define ARRAY_SIZE  10

int a = 7;
unsigned long b = 8;
short c;
char x;
char* pc;

int array1[ARRAY_SIZE];
int array2[a]; 

char* cadena1 = "CADENA DE CARACTERES";	
char cadena2[] = "CADENA DE CARACTERES";
int main() {
	pc =&x;
	a = 16;
	printf("Adress of a: %p Tam: %lu \n",&a,sizeof(a));
	printf("Adress of b: %p Tam: %lu \n",&b,sizeof(b));
	printf("Adress of c: %p Tam: %lu \n",&c,sizeof(c));
	printf("Adress of x: %p Tam: %lu \n",&x,sizeof(x));
	printf("Adress of pc: %p Adress pointed by pc: %p Tam: %lu \n",&pc,pc,sizeof(pc));
	printf("Adress of array: %p Adress of elem 0: %p Tam de array: %lu \n",array1, &array1[0], sizeof(array1));
	printf("Adress of cadena1: %p Adress pointed by: %p Tam: %lu \n",&cadena1,cadena1,sizeof(cadena1));
	printf("Adress of cadena2: %p DAdress pointed by: %p Tam: %lu \n",&cadena2,cadena2,sizeof(cadena2));	
return 0;
}
```

## Using Arrays.
```c 
#include <stdio.h>

/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 * 1. Should we use "&list" to get the address of the array?
 * 2. What is actually stored in the address of "list"?
 * 3. Why are we including the lentgh of the array as parameter to "init_array"?
 * 4. Why the sizeof() output is different for the array in "init_array" and the one in main()?
 * 5. Why aren't we including a second parameter in init_array2?
 * 6. Do sizeof() outuput now match with the array in init_array2()?
 ***************/

#define N 5

void init_array(int array[], int size) ;
void init_array2(int array[N]);

int main(void) {
	int i,list[N];
	printf("Dir de list %p Dir de list[0]: %p  Dir de list[1]: %p. Sizeof list %lu \n",list,&list[0],&list[1],sizeof(list));
	
	init_array(list, N);
	for (i = 0; i < N; i++)
		printf("next: %d ", list[i]);
	printf("\n-------------------------\n");

	init_array2(list);
	for (i = 0; i < N; i++)
		printf("next: %d ", list[i]);
	printf("\n-------------------------\n");
}

void init_array(int array[], int size) { 
	int i;
	printf("Direccion de array: %p Sizeof array %lu \n", array, sizeof(array));
	for (i = 0; i < size; i++)
		array[i] = i;
	printf("Array initialized\n\n");
}

void init_array2(int array[N]) { 
	int i;
	printf("Direccion de array: %p Sizeof array %lu \n", array, sizeof(array));
	for (i = 0; i < N; i++)
		array[i] = i*2;
	printf("Array initialized\n\n");
}
```

```c
#include <stdio.h>

/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 *  1. Does the copy of the array works? Why? 
 *  2. Fix it.
 *  3. Uncommnet the call to function "tom". Compile again and execute.
 *  4. The problem that arises, is it in compilation or execution time? Why?
 *  5. Find a value for MAXVALID (greater than 4) when the problem does not happen. Why does it work?
*******************/

#define N 10
#define MAXELEM 5000
#define MAXVALID 100

void printArray(int v[],int size) {
	int i;
	printf("-------------------\n");
	for (i=0;i<size;i++)
		printf("%d ",v[i]);
	printf("\n\n");

}

void copyArray(int src[],int dst[],int size) {
 	dst = src;
}

void tmo() {
	int x = -1; 
	int a[4] = {0,1,2,3};	 
	int b = 10000;
	int c = -1;
	int i;

	for  (i=4;i<MAXVALID;i++)
		a[i]=i;

	printf("x %d b %d c %d\n", x,b,c);

			
}

int main() {
	int A[N] = {4,3,8,5,6,9,0,1,7,2};
	int B[N];
	
	//tmo();
	copyArray(A,B,N);
	printArray(B,N);
		
}
```

## Pointers
```c

#include <stdio.h>
#include <stdlib.h>

/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 * 1. Which operand should we use to declae a variable as a ponter?
 * 2. How do we obtain the address of a variable?
 * 3. How do we read/write into the address pointed by a pointer? 
 * 4. There ¡s a bug in the code. Is it a compile-time or executiontime errror? Why does it happen?
  ***********/
int c = 7;
int main(void) {

	int *ptr;
	printf("Address of ptr %p. ptr apunta a %p. Address of c: %p Valor of c %d\n",&ptr,ptr,&c,c);	

	ptr = &c;
	printf("Address of ptr %p,. ptr apunta a %p. Address of c: %p Value of c %d\n",&ptr,ptr,&c,c);	
	
	*ptr=4;
	printf("ptr apunta a %p. Content of address of ptr: %d Address of c: %p Value of c %d\n",ptr,*ptr,&c,c);	

	ptr =  (int*) 0x600a48;
	printf("Address of ptr %p. Value of c %d\n",ptr,c);	
	
	*ptr =13;
	printf("Address of ptr %p. Value of c %d\n",ptr,c);	

return 0;
	
}
```

```c
#include <stdio.h>
#include <stdlib.h>

/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 *  1. How many bytes are allocated in memory with the malloc() call?
 *  2. Which are the addresses of the first and last bytes of the allocated area?
 *  3. Why the content of the address pointed by "ptr" is 7 and not 5 in the first printf()?
 *  4. Why the content of ptrg[1] is modified after the sentence *ptr2=15 ?
 *  5. Suggest two different ways of writting the value 13 in the address of ptr[100] 
 *  6. There is a bug in the code. Even if nothing goes wrong,the bug is there. Where?
 *  ***********/
int nelem;

int main(void) {
	int *ptr;
	int * ptr2;	

	nelem = 127;
	ptr = (int*) malloc(nelem*sizeof(int));
	*ptr = 5;
	ptr[0] = 7;
	ptr2 = ptr;

	printf("Address pointed by ptr %p. Content of that address: %d \n",ptr,*ptr);	

	ptr[1] = 10;	
	printf("Address pointed by ptr[1] %p. Content of that address: %d \n",&ptr[1],ptr[1]);	

	ptr2++;
	*ptr2 = 15;
	printf("Address pointed by ptr[1] %p. Content of that address: %d \n",&ptr[1],ptr[1]);	


	free(ptr);	
	*ptr = 3;
	printf("Address pointed by ptr %p. Content of that address: %d \n",ptr,*ptr);	
}
```

```c
#include <stdio.h>
#include <stdlib.h>
/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 *  1. Why the value of ptr[13] is changed after the sentence ptr = &c;
 *  2. This code has (at least) one bug. Compile or run-timer error? Why?
 *  3. What happens with the memory allocated by malloc()  after the assignment ptr=&c? 
 *     How can we reach that memory again? How can we free it?
 *  ***********/
int nelem;
int c;
int main(void) {
	int *ptr;
	int i;
	c = 37;	
	nelem = 127;
	ptr = (int*) malloc(nelem*sizeof(int));
	for (i=0; i<nelem; i++)
		ptr[i] = i;

	printf("ptr[0]= %d ptr[13]=%d \n",ptr[0],ptr[13]);	

	ptr = &c;
	printf("ptr[0]= %d ptr[13]=%d \n",ptr[0],ptr[13]);	

	free(ptr);
}
```
```c
#include <stdio.h>
#include <stdlib.h>
/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 *  1. Why the second printf() prints a different value for 'd'?
 *  2. What is 'f'? A variable? A function?
 *  3. Use the function 'opera()' to perform the first addition. Then, use it again to perform a substraction.
 *  4. Using typedef, build a type called ptrToFunc with the same prototype thatn 'f'
 *  5. Creat a function 'choose()' that will return, alternatively, a pointer to "add()" and "sub()" 
 *     every time it is called
 *  ***********/

int add (int x, int y);
int sub(int x, int y);

int (*f)(int a, int b);

int add(int x, int y) {
	return x+y;
}

int sub(int x, int y) {
	return x-y;
}

int opera(int x, int y, int (*g)(int, int)) {
	return g(x,y);
}

int main(void) {

	int a = 12;
	int b =	 8;
	int c,d;

	f = add;
	c = add(a,b);
	d = f(a,b);
	printf("c = %d d= %d \n",c,d);	
	f = sub;
    d = f(a,b);
	printf("c = %d d= %d \n",c,d);
}
```

## Arguments

```c
#include <stdio.h>
/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 * 1. Why the value of 'xc' is not changed after the call to sumC()? 
 *     Where do the write operations happen?
 * 2. Comment  the two forwarded declarations of sum() and sumC(). Compile again. What happens?
 *******************/
/* Struct type */
struct _complex_ {
	float re;
	float im;
};

/* Forward declarations */
int sum(int a, int b);
struct _complex_  sumC( struct _complex_ a,  struct _complex_ b);


int main(void){
	int x = 4,y = 5;
	struct _complex_  xc = {.re = 1.0, .im = 2.0};
	struct _complex_  yc = {.re = 3.0, .im = 1.0};
	struct _complex_  zc; 

	zc = sumC(xc,yc);

	int total = sum(x,y); 
	
	printf("Suma de complejos. (%f,%f i) + (%f,%f i) =(%f,%f i)\n",xc.re,xc.im,yc.re,yc.im,zc.re,zc.im);
	printf("Suma de enteros:  x +y = %d + %d = %d \n",x,y, total);
	return 0;
}

int sum(int x, int y) {  
	int c;
	c = x +y;
	x = 7;
	y =3;  
	return c;         
}


struct _complex_  sumC( struct _complex_ a,  struct _complex_ b) {
		struct _complex_ r;
		r.re = a.re + b.re;
		r.im = a.im + b.im;
		// Try to change the first parameter
		a.re = 12.5;
		a.im = 13.4;
		return r;
}
```
```c
#include <stdio.h>
/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 * 1. Why does the value of 'y' changes after the call to sum()?
 * 2. Why sometimes we use operator '.' and other times '->'?
 * 3. Why the vauue of 'zc' gets wrong without further using it in the code?
 * 4. Fix the code to avoid the bug in 'zc' shown in previous point
 *******************/
struct _complex_ {
	float re;
	float im;
};

int sum(int *pa, int *pb);
struct _complex_ * sumC( struct _complex_ *a,  struct _complex_ *b);


int main(void){
	int x = 4,y = 5;
	int* ptr = &y;
	struct _complex_  xc = {.re = 1.0, .im = 2.0};
	struct _complex_  yc = {.re = 3.0, .im = 1.0};
	struct _complex_  *zc; 


	printf("Complex addition (%f,%f i) + (%f,%f i) = ", 	xc.re,xc.im,yc.re,yc.im);
	zc = sumC(&xc,&yc);
	printf("(%f,%f i)\n",zc->re,zc->im);
	int total = sum(&x,ptr); 

	printf("Complex addition:  x +y = %d + %d = %d \n",x,y, total);
	printf("xc = (%f,%f i)  yc = (%f,%f i) zc = (%f,%f i)\n",xc.re,xc.im,yc.re,yc.im,zc->re,zc->im);
	return 0;
}

int sum(int *pa, int *pb) {  
   /* args passed by reference */
  int c = *pa + *pb;
  int buf[256] = {0};
  *pa = 7;
  *pb = 8;	
   return c;      /* return by value */
}


struct _complex_ * sumC( struct _complex_* a,  struct _complex_* b) {
		struct _complex_ r;
		r.re = a->re + b->re;
		r.im = a->im + b->im;
		a->re = 12.5;
		a->im = 13.4;
		return &r;
}
```

## Strings

```c 
#include <stdio.h>
#include <string.h>

/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 * 1. The code has a bug. Compile or run-time? Why?
 * Fix the bug commenting the line(s) that produce it. Compile and execute again. 
 * 2. Which is the address of letter 'B' in the chain "Bonjour"? And letter 'j'?
 * 3. After the assignment p=msg2; how can we get back the address of "Bonjour"?
 * 4. Why the length of strings 'p' and 'msg2' are 2 after the third assignment?
 *    3 bytes are assigned to 'p', but then the length is only 2 !!
 * 5. Why strlen() returns a different value than sizeof()?
 * 6. Why the string stored in 'msg' in line 36 is bad-printed in the last printf()?
 ************** */
int main() {

char msg[10]; /* array of 10 chars */
char *p;          /* pointer to a char */

char msg2[28]="Hello";  /* msg2 = 'H' 'e' 'l' 'l' 'o' '\0' */
     
	p   = "Bonjour"; 
	printf("msg: %s, p: %s, msg2: %s\n",msg,p,msg2);
	printf("dir de msg: %p, dir de p: %p, dir de msg2: %p\n",msg,p,msg2);

	p = msg2;
	printf("msg: %s, p: %s, msg2: %s\n",msg,p,msg2);
	printf("dir de msg: %p, dir de p: %p, dir de msg2: %p\n",msg,p,msg2);

 	p[0] = 'H', p[1] = 'i',p[2]='\0';
	printf("msg: %s, p: %s, msg2: %s\n",msg,p,msg2);
	printf("msg len: %lu p len %lu msg2 len %lu\n", strlen(msg),strlen(p),strlen(msg2));
	printf("msg size: %lu p size %lu msg2 size %lu\n", sizeof(msg),sizeof(p),sizeof(msg2));

	msg[0] = 'B', msg[1] = 'y';
	printf("msg: %s, p: %s, msg2: %s\n",msg,p,msg2);

	msg = "Goodbye";
	printf("msg: %s, p: %s, msg2: %s\n",msg,p,msg2);
}
```
```c
#include <stdio.h>
#include <string.h>

/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 * 1. The code of fcuntion 'copy' does not work. Why?
 * 2. Use now 'copy2()'. Does the copy actually work?
 * 3. Suggest a valid implementation for a copy
 * 4. What does function "mod" do? 
 * 5. Uncomment last line of code (call to mod()). Compile and execute. Why is there an error now?
 ************** */

void copy2(char* org, char** dst) {
	*dst = org;
}

void copy(char* org, char* dst) {
	dst = org;
}

void mod(char* org, char* dst) {
	int i;

	for (i=0;i<strlen(org);i++)
		dst[i] = org[i] - 32;

}

int main() {

	char* cad1 = "original";          
	char* cad2 = "other";
	char cad3[32];

	copy(cad1,cad2);
	//copy2(cad1,&cad2);
	printf("cad1 %s cad2 %s\n", cad1,cad2);

	mod(cad1,cad3);
	printf("cad1 %s cad3 %s\n", cad1,cad3);
	
	//mod(cad1,cad1);
}
```
## Bitwaise operations

```c
#include <stdio.h>

/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 * Study the syntax of the different bit-level operators
 * and make sure you understand  the result of every operation
 ************** */

int a,b,c;

int main() {

	a = 7;
	b = 9;
	c = a & b;
	printf("%x AND %x = %x\n",a,b,c);

	c= a | b;
	printf("%x OR %x = %x\n",a,b,c);

	c = a ^ b;
	printf("%x XOR %x = %x\n",a,b,c);

	c = ~a;
	printf("NOT %x = %x\n",a,c);

	c = a << 2;
	printf(" %x << 2 = %x\n",a,c);

	c = a >> 1;
	printf(" %x >> 1 = %x\n",a,c);

	c = a & 0xFB;
	printf(" %x bit 2 to 0 -> %x\n",a,c);

	c = a | 0x40;
	printf(" %x bit 6 to 1 -> %x\n",a,c);

	c = (a & 0x1C) >> 2;
	printf("bits 4-3-2 of %x: %x\n",a,c);	
}
```

```c
#include <stdio.h>

/**** QUESTIONS/TASKS ********
 * Compile and execute the code. 
 * 1. Why the assignment using pointer 'p' does not overwrite completely 'a'?
 * 2. How is modified the address pointed by 'p' after the assignment p=p+1
 * 3. How would it be different if 'p' is declared as 'short *'
 *
 ************** */
int a = 3;
int b;
char * p;
int c;
int main() {

	printf("a = %x Address of a: %p \n",a,&a);
	p = (char*) &a;
	p=p+1;
	*p= 0x1f;
	printf("a = %x. Address pointed by p:%p \n",a,p);
	
	a = 3;
	b = 0x00001f00;
	a= a | b;
	
	printf("a = %x. Address pointed by p:%p \n",a,p);
}
```

