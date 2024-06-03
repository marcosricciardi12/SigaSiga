import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DirectorPage } from './director.page';

describe('DirectorPage', () => {
  let component: DirectorPage;
  let fixture: ComponentFixture<DirectorPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(DirectorPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
