import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ExamenService } from '../../service/examen.service';
import { CategoriaService } from '../../service/categoria.service';
import { NivelService } from '../../service/nivel.service';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-buscar-examenes',
  standalone: true,
  imports: [CommonModule, FormsModule,RouterModule],
  templateUrl: './buscar-examenes.component.html',
  styleUrl: './buscar-examenes.component.css'
})
export class BuscarExamenesComponent implements OnInit {

  examenes: any[] = [];

  categorias: any[] = [];
  niveles: any[] = [];

  filtros = {
    categoria: '',
    nivel: '',
    creador: '',
    search: ''
  };

  constructor(
    private examenService: ExamenService,
    private categoriaService: CategoriaService,
    private nivelService: NivelService
  ) {}

  ngOnInit(): void {
    this.cargarFiltros();
    this.buscarExamenes();
  }

  cargarFiltros() {
    this.categoriaService.getCategorias().subscribe(data => {
      this.categorias = data;
    });

    this.nivelService.getNiveles().subscribe(data => {
      this.niveles = data;
    });
  }

  buscarExamenes() {
    this.examenService
      .getExamenesFiltrados(
        this.filtros.categoria,
        this.filtros.nivel,
        this.filtros.creador
      )
      .subscribe(data => {
        this.examenes = data;
      });
  }

  limpiarFiltros() {
    this.filtros = {
      categoria: '',
      nivel: '',
      creador: '',
      search: ''
    };

    this.buscarExamenes();
  }
}