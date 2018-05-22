import { MaterializeModule } from 'angular2-materialize';

import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { Router } from '@angular/router';

import { HttpClientModule } from '@angular/common/http';

import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { MainComponent } from './main/main.component';
import { AboutUsComponent } from './about-us/about-us.component';
import { ResultSearchComponent } from './result-search/result-search.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { InputSearchComponent } from './input-search/input-search.component';
import { AppRoutingModule } from './app-routing.module';
import { ResultsComponent } from './results/results.component';
import {SearchingService} from "./searching-service.service";

@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    AboutUsComponent,
    ResultSearchComponent,
    NotFoundComponent,
    InputSearchComponent,
    ResultsComponent
  ],
  imports: [
    MaterializeModule,
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [SearchingService],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(router: Router) {
  }
}
