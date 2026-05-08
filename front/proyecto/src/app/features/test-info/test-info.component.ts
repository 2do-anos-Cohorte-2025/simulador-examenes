import { Component } from '@angular/core';

@Component({
  selector: 'app-test-info',
  standalone: true,
  imports: [],
  templateUrl: './test-info.component.html',
  styleUrl: './test-info.component.css'
})
export class TestInfoComponent {
   
  checkUrl: string = 'assets/icons/checkbox.svg';
}
