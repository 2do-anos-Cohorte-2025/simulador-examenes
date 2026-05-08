import { Component } from '@angular/core';
import { ExamFormComponent } from '../../components/exam-form/exam-form.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [ExamFormComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {

}
