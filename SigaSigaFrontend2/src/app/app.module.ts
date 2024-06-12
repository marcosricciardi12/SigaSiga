import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy } from '@ionic/angular';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { AuthService } from './services/auth.service';
import { VideoStreamService } from './services/videostream.service';
import { ConfigTimeModalComponent } from './config-time-modal/config-time-modal.component';
import { FormsModule } from '@angular/forms'; // Agrega esta línea

@NgModule({
  declarations: [AppComponent, ConfigTimeModalComponent],
  imports: [BrowserModule, IonicModule.forRoot(), AppRoutingModule, HttpClientModule, FormsModule],
  providers: [{ provide: RouteReuseStrategy, useClass: IonicRouteStrategy }, AuthService, VideoStreamService],
  bootstrap: [AppComponent],
})
export class AppModule {}
