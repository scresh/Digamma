import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { MainComponent } from './main/main.component';
import { AboutUsComponent } from './about-us/about-us.component';
import { ResultSearchComponent } from './result-search/result-search.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { InputSearchComponent } from './input-search/input-search.component';


@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    AboutUsComponent,
    ResultSearchComponent,
    NotFoundComponent,
    InputSearchComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
