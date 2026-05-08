import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeroComponent } from '../../shared/hero/hero.component';
import { TestCardComponent } from '../../features/test-card/test-card.component';
import { TestInfoComponent } from '../../features/test-info/test-info.component';



@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [RouterOutlet, HeroComponent, TestCardComponent, TestInfoComponent],
  templateUrl: './inicio.component.html',
  styleUrl: './inicio.component.css'
})
export class InicioComponent {

}
