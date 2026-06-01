import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IntentoExamenComponent } from './intento-examen.component';

describe('IntentoExamenComponent', () => {
  let component: IntentoExamenComponent;
  let fixture: ComponentFixture<IntentoExamenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [IntentoExamenComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(IntentoExamenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
