import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
@Component({
  selector: 'app-categoria-card',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './categoria-card.component.html',
  styleUrl: './categoria-card.component.css'
})
export class CategoriaCardComponent {
    arrowUrl: string = 'assets/icons/arrow-up.svg';
  testsCardList: { id: number, titulo: string; imagen: string; alt: string }[] = [
{ id:1, titulo: "Ciencias Naturales", imagen:"/assets/carousel/card-ciencias.png", alt:"Card de ciencias naturales",},
{ id:2, titulo: "Digital", imagen:"/assets/carousel/card-educacion.png", alt:"Card de digital",},
{ id:3, titulo: "Literatura", imagen:"/assets/carousel/card-escritura.png", alt:"Card de literatura",},
{ id:4, titulo: "Lenguaje", imagen:"/assets/carousel/card-lenguaje.png", alt:"Card de lenguaje",},
{ id:5, titulo: "Matemática", imagen:"/assets/carousel/card-matematica.png", alt:"Card de matemática",},
{ id:6, titulo: "Física", imagen:"/assets/carousel/card-primario.png", alt:"Card de física",},
{ id:7, titulo: "Ciencias Sociales", imagen:"/assets/carousel/card-sociales.png", alt:"Card de ciencias sociales",},
{ id:8, titulo: "Otros", imagen:"/assets/carousel/card-quizz.png", alt:"Card de otros",},
]; 
}
