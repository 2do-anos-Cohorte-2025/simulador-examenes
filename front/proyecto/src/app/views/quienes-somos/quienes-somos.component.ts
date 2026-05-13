import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-quienes-somos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './quienes-somos.component.html',
  styleUrl: './quienes-somos.component.css'
})
export class QuienesSomosComponent {

  integrantes = [
    {
      nombre: 'Lucía Abigail Chavez Sosa',
      rol: 'Desarrolladora Web',
      imagen: '../assets/team/Lucia.jpg',
      github: 'https://github.com/lucia8307'
    },
    {
      nombre: 'Pablo Valentín Sosa Luque',
      rol: 'Desarrollador Web',
      imagen: '../assets/team/Valentin.jpg',
      github: 'https://github.com/ValentixoRandom'
    },
    {
      nombre: 'Cristian Felipe Pasquevich',
      rol: 'Desarrollador Web',
      imagen: '../assets/team/Cristian.jpg',
      github: 'https://github.com/CristianPasquevich'
    },
    {
      nombre: 'Leandro Manuel Quiroga Perez',
      rol: 'Desarrollador Web',
      imagen: '../assets/team/Leandro.jpg',
      github: 'https://github.com/LeandroQuiroga7'
    },
    {
      nombre: 'Luciano Nazareno Di Leo Rodriguez',
      rol: 'Desarrollador Web',
      imagen: '../assets/team/Luciano.png',
      github: 'https://github.com/D-LucianoDiLeo'
    },
    {
      nombre: 'Lara Gele',
      rol: 'Desarrolladora Web',
      imagen: '../assets/team/Lara.jpg',
      github: 'https://github.com/laragele2005'
    }
  ];

}
