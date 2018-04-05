class Person {
  name: string;
  activity: string;
  slogan: string;
  image: string;

  constructor(name: string, activity: string, slogan: string, image: string){
    this.name = name;
    this.activity = activity;
    this.slogan = slogan;
    this.image = '../../assets/aboutUs/'+image;
  }
}

export const we = [
  new Person("Manos", "Kierownik - Wizjoner - Programista Python - Specjalista ToR", "","default.jpg"),
  new Person("Fiszcz", "Wizjoner - Front-End - Serwer", "Kontakt: fiszczu@gmail.com","fs.jpg"),
  new Person("Yamatano", "Front-End - Baza Danych - Serwer","","aw.jpg"),
  new Person("Miki", "Programista Python", "","mt.jpg"),
  new Person("Mati", "Programista Python", "","ms.jpg"),
  new Person("Maciej", "Na razie nic", "","default.jpg")
];
