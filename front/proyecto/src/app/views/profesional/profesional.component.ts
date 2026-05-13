// Función pensada a futuro si queremos añadir más información sobre cada integrante más que el Github

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-profesional',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './profesional.component.html',
  styleUrl: './profesional.component.css'
})
export class ProfesionalComponent implements OnInit {

  id: string | null = '';

  profesionales: any = {
    1: {
      nombre: 'Federico Gonzales',
      rol: 'Desarrollador Web',
      descripcion: 'Especializado en frontend y backend.',
      imagen: 'assets/team/Cristian.jpg'
    },

    2: {
      nombre: 'Diana López',
      rol: 'Desarrolladora Web',
      descripcion: 'Apasionada por Angular y UX/UI.',
      imagen: 'assets/team/2.jpg'
    },

    3: {
      nombre: 'Joaquín Aguirre',
      rol: 'Diseñador Gráfico',
      descripcion: 'Encargado de la identidad visual.',
      imagen: 'assets/team/3.jpg'
    }
  };

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.id = this.route.snapshot.paramMap.get('id');
  }

}
