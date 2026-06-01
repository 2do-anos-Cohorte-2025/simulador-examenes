import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExamenPreguntaComponent } from './examen-pregunta.component';

describe('ExamenPreguntaComponent', () => {
  let component: ExamenPreguntaComponent;
  let fixture: ComponentFixture<ExamenPreguntaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExamenPreguntaComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ExamenPreguntaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
