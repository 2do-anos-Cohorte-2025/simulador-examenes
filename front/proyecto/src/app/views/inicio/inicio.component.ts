import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeroComponent } from '../../shared/hero/hero.component';
import { CategoriaCardComponent } from '../../components/categoria-card/categoria-card.component';
import { InformacionTestAceComponent } from '../../components/informacion-test-ace/informacion-test-ace.component';



@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [RouterOutlet, HeroComponent,  CategoriaCardComponent, InformacionTestAceComponent],
  templateUrl: './inicio.component.html',
  styleUrl: './inicio.component.css'
})
export class InicioComponent {

}
