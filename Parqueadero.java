/**
 * Clase principal del programa, en donde están los métodos Parqueadero, ingresarDatos, parquearCarro, sacarCarro, estadoCarro, estadoParqueadero, menu y crearCarro.
 * @autor Santiago Sabogal y Emmanuel Hernández
 */
/**
 * 
 */
import java.util.Scanner;

public class Parqueadero {
    private int recaudado = 0; //Lo recaudado por el parquedero en general
    private int pisos; //pisos del parqueadero
    private int espaciosPorPiso; //Celdas que hay en cada piso del parqueadero
    private Carros[][] ocupado; // Usamos la clase Carros en lugar de boolean

    Scanner sc = new Scanner(System.in); //Instanciación del Scanner
    int opc1; //Variable utilizada en el switch del menú
    int opc2;
    int opc3;
    
    
    /**
     * El método Parqueadero lo que hace es llamar al método
     * ingresar datos para después instanciar la matrís e igualarla con la variable ocupado,
     * para así actualiazar el dato de la matríz del parqueadero
     */
    public Parqueadero() {
        ingresarDatos();
        this.ocupado = new Carros[pisos][espaciosPorPiso]; // Cambiamos el tipo de la matriz
    }
    
    /**
     * El método main de la clase en este caso solo se limita a ejecutar el método parqueadero
     */
    public static void main(String[] args) {
        Parqueadero parqueadero = new Parqueadero(); //Se ejecuta el método parqueadero por medio de la instanciación parqueadero
    }
    
    /**
     * En este método lo que se hace es que se le pide al usuario que cree la matríz del parqueadero,
     * es decir, que diga cuantos pisos tendrá el parqueadero y cuantas celdas habrá en cada uno de estos
     */
    private void ingresarDatos() {
        System.out.print("Ingrese cantidad de pisos: ");
        this.pisos = sc.nextInt();

        System.out.print("Ingrese cantidad de espacios por piso: ");
        this.espaciosPorPiso = sc.nextInt();
    }
    
    /**
     * Este método lo que hace es que cuando se ejecuta este ubica al vehículo en cuestión en a celda libre más inmediata, empezando dese abajo.
     */

    public boolean parquearCarro(Carros carro) {
        for (int piso = 0; piso < ocupado.length; piso++) { //For's que recorren la matriz de parqueadero
            for (int celda = 0; celda < ocupado[piso].length; celda++) {
                if (ocupado[piso][celda] == null) { // Verificamos si la posición está vacía
                    ocupado[piso][celda] = carro; // Asignamos el objeto carro en la posición
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * Método que sirve para eliminar el carro de la matríz en la ubicación que marca el usuario, este
     * también calcula lo que el carro a eliminar deberá pagar en base a la hora de entrada y la hora
     * de salida digitada por el usuario
     */

    public void sacarCarro() {
        System.out.print("Ingrese piso del vehiculo a sacar: ");
        int piso = sc.nextInt();
        System.out.print("Ingrese espacio del vehiculo a sacar: ");
        int espacio = sc.nextInt();
        //Identificar el vehículo por medio de la celda en la que esté para eliminarlo

        if (piso >= 0 && piso < ocupado.length && espacio >= 0 && espacio < ocupado[piso].length) { //Se verifica que la posición digitada por el usuario esté dentro de la matríz
            if (ocupado[piso][espacio] != null) {
                Carros carro = ocupado[piso][espacio]; //Instanciación de la matríz carro
                ocupado[piso][espacio] = null; //se elimina al vehículo
                String horaEntrada = carro.getHoraEntrada(); // Obtener el valor de horaEntrada
                int hEntrada = Integer.parseInt(horaEntrada); //La horaentrada estaba como una variable String, a
                System.out.print("Hora de salida (en hora militar): ");
                int hSalida = sc.nextInt();

                int hestadia = hSalida - hEntrada; //
                int hapagar = hestadia/100;
                int minutosRestantes = hestadia % 100; //ver si hay residuo en

                if (minutosRestantes > 0) {
                    hapagar++; // Redondear hacia arriba si hay minutos restantes
                }

                int pago = hapagar * 1000; //1000 pesos por fracción de hora

                recaudado += pago; //Se añade el pago del vehículo en cuestión a lo recaudado por el parqueadero

                System.out.println("Vehiculo sacado exitosamente: " + carro.getMatricula() + ", tendrá que pagar "+hapagar+" horas por un valor de " + pago + " pesos, tenga un buen día");

            } else {
                System.out.println("No hay un vehiculo en la posición especificada");
            }
        } else {
            System.out.println("La posición especificada no es válida");
        }
    }

    /**
     * Método que tiene la funcion de decirle al usuatrio, en base a la placa la ubicación de este en la
     * matríz del parqueadero
     */
    public void estadoCarro() {
        Scanner sc = new Scanner(System.in);
        System.out.println("Ingrese la placa de su vehiculo: ");
        String placa = sc.nextLine();

        boolean encontrado = false;

        for (int piso = 0; piso < ocupado.length; piso++) {
            for (int celda = 0; celda < ocupado[piso].length; celda++) {
                Carros carro = ocupado[piso][celda];
                if (carro != null && carro.getMatricula().equals(placa)) {
                    System.out.println("Su vehiculo está en la posición: Piso " + piso + ", Celda " + celda);
                    encontrado = true;
                    break;
                }
            }
            if (encontrado) {
                break;
            }
        }

        if (!encontrado) {
            System.out.println("No se encontró ningún vehiculo con la placa especificada");
        }

    }
    
    /**
     * Método que sirve para que el usuario sepa si hay celdas libres en el parqueadero
     * y lo que ha recaudado el parqueadero hasta el momento
     */
    public void estadoDelParqueadero() {  
        int celdasOcupadas = 0;
        int celdasVacias = 0;

        for (int piso = 0; piso < ocupado.length; piso++) {
            for (int celda = 0; celda < ocupado[piso].length; celda++) {
                if (ocupado[piso][celda] != null) {
                    celdasOcupadas++;
                } else {
                    celdasVacias++;
                }
            }
            System.out.println("En el piso " + piso + " hay " + celdasOcupadas + " celdas ocupadas, y " + celdasVacias + " celdas libres");
            celdasOcupadas = 0; // Reiniciar el contador de celdas ocupadas para el siguiente piso
            celdasVacias = 0; // Reiniciar el contador de celdas libres para el siguiente piso
        }
        System.out.println("El parqueadero a generado " + recaudado + " pesos en general");
    }

    /**
     * Método en el que se le muestra al usuario todo lo que puede hacer con el código y por consecuencia ejecutarlo por medio de un switch y sus casos
     */
    public void menu() {
        do {
            System.out.println("0. Salir del programa");
            System.out.println("1. Ingresar vehiculo");
            System.out.println("2. Sacar vehiculo");
            System.out.println("3. Estado del vehiculo");
            System.out.println("4. Estado del parqueadero");
            opc1 = sc.nextShort();

            switch (opc1) {
                case 0:
                    System.out.println("Saliendo del programa ...");
                    break;
                case 1:
                    System.out.println("Ingrese datos del vehiculo:");
                    Carros carro = crearCarro(); // Llamamos a un método para crear un objeto Carros
                    boolean ingresado = parquearCarro(carro); // Llamamos a parquearCarro con el objeto Carros creado
                    if (ingresado) {
                        System.out.println("Vehiculo ingresado exitosamente");
                    } else {
                        System.out.println("No hay espacios disponibles para ingresar el vehiculo");
                    }
                    break;
                case 2:
                    System.out.println("Ingrese piso y espacio del vehiculo a sacar:");
                    sacarCarro();
                    break;
                case 3:
                    System.out.println("Mostrando estado del vehiculo:");
                    estadoCarro();
                    break;
                case 4 :
                    System.out.println("Estado del parqueadero: ");
                    estadoDelParqueadero();
                    break;
                    
                case 5 :
                    switch(opc2){
                        case 0:System.out.println( "salir");
                        break;
                        
                        case 1:System.out.println("prededador");
                        switch (opc3){
                            case 0: System.out.println( "salir");
                            break;
                            
                            case 1: System.out.println( "movimiento adelante:");
                            
                            
                        }
                        
                        
                    }
                default:
                    System.out.println("Opción inválida");
                    break;
            }
        } while (opc1 != 0);
    }

    /**
     * Metodo que manda los datos a la clase carros para que los instance con getter y setter
     */

    private Carros crearCarro() {
        Scanner sc = new Scanner(System.in);
        System.out.print("Ingrese la matricula del vehiculo: ");
        String matricula = sc.nextLine();
        System.out.print("Ingrese el color del vehiculo: ");
        String color = sc.nextLine();
        System.out.print("Ingrese la hora de entrada del vehiculo (horario militar): ");
        String horaEntrada = sc.nextLine();
        //Se piden cada uno de los datos necesarios de el vehículo, es decir, matrícula, color y la hora de entrada
        return new Carros(matricula, color, horaEntrada);
    }

}

