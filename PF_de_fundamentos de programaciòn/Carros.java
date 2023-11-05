
/**
 * Clase carros en donde se almasenan las variables matrícula, color y horaEntrada y  se actualizan por medio de getter y setter
 */

public class Carros{
    private String matricula;
    private String color;
    private String horaEntrada;

    public Carros(String matricula, String color, String horaEntrada) {
        this.matricula = matricula;
        this.color = color;
        this.horaEntrada = horaEntrada;
    }

    // Métodos getter y setter para los atributos

    public String getMatricula() {
        return matricula;//Se actualiza el valor de la matrícula del carro
    }

    public void setMatricula(String matricula) { //Se igualan las variables para que no sean dos con dos valores diferentes
        this.matricula = matricula;
    }

    public String getColor() { //Se actualiza el dato del color del carro
        return color;
    }

    public void setColor(String color) {
        this.color = color; //Se igualan las variables para que no sean dos con dos valores diferentes
    }

    public String  getHoraEntrada() {
        return horaEntrada;//Se actualiza el ato de la hora de entrada del vehículo
    }

    public void setHoraEntrada(String horaEntrada) {
        this.horaEntrada = horaEntrada;//Se igualan las variables para que no sean dos con dos valores diferentes
    }
}

