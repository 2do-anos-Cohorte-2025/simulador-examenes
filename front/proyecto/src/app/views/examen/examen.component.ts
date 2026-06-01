import { Component } from '@angular/core';
import { ExamenInfoComponent } from '../../components/examen-info/examen-info.component';

@Component({
  selector: 'app-examen',
  standalone: true,
  imports: [ExamenInfoComponent],
  templateUrl: './examen.component.html',
  styleUrl: './examen.component.css'
})
export class ExamenComponent {

}
