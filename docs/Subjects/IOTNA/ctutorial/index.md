# C programming. Exercises


There are many good C/C++ tutorials online. You can find one in [this link](https://www.cprogramming.com/tutorial/c-tutorial.html).

Next, there are several examples that we will use during the lectures to talk about different aspects of C language.


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
 * 2. How largeais a 'char' variable?
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
 * 4. What does the modifer "%lu" means in printf()? 
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
 * 5. Why aren't we inclugind a second parameter in init_array2?
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

// funcion que imprime por pantalla el conteniod del array v de tam. size
void imprimeArray(int v[],int size) {
	int i;
	printf("-------------------\n");
	for (i=0;i<size;i++)
		printf("%d ",v[i]);
	printf("\n\n");

}

// funcion que copia el contenido de un array en otro
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
	imprimeArray(B,N);
		
}
```
