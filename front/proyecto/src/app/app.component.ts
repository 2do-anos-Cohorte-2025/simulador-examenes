import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './shared/header/header.component';
import { FooterComponent } from './shared/footer/footer.component';
import { HeroComponent } from './shared/hero/hero.component';
import { TestCardComponent } from './features/test-card/test-card.component';
import { TestInfoComponent } from './features/test-info/test-info.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HeaderComponent,FooterComponent, HeroComponent, TestCardComponent, TestInfoComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'proyecto';
 
}
