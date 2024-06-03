import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { DirectorPageRoutingModule } from './director-routing.module';

import { DirectorPage } from './director.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    DirectorPageRoutingModule
  ],
  declarations: [DirectorPage]
})
export class DirectorPageModule {}
