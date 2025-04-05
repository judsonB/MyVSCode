public class Warrior 
{
  private String name;
  private int str;
  private int def;
  private int hp;
  public Warrior()
  {
    name = "John Smith";
    str = (int)(Math.random() * 20)+1;
    def = (int)(Math.random() * 20)+1;
    hp = (int)(Math.random() * 20)+80;
  }
  public Warrior(String name, int str, int def, int hp)
  {
    this.name = name;
    this.str = str;
    this.def = def;
    this.hp = hp;
  }
    public String getName()
    {
      return name;
    }
    public int getStr()
    {
      return str;
    }
    public int getDef()
    {
      return def;
    }
    public int getHp()
    {
      return hp;
    }

    public void setName(String name)
    {
      this.name = name;
    }
    public void setStr(int str)
    {
      this.str = str;
    }
    public void setDef(int def)
    {
      this.def = def;
    }
    public void setHp(int hp)
    {
      this.hp = hp;
    }
  public String toString()
  {
    String msg = "";
    msg += "Warrior: "+name;
    msg += "\n    Str: "+str;
    msg += "\n    Def: "+def;
    msg += "\n    HP : "+hp;
    return msg;
  }
  //Helper Functions
  public void attack(Warrior other)
  {
    //Generate a random value from 1 to str
    int atk = random_range(1, this.str);
    //Generate a random value from 1 to other's def
    int block = random_range(1, other.def);
    //if atk > block --> other's hp decreases by the difference
    int dif = atk - block;
    if(dif > 0)
    {
      System.out.println(this.name + " hit "+other.name+" dealing "+dif+" damage.");
      other.hp -= dif;
    }
    else
    {
      System.out.println(this.name + "'s hit towards "+other.name+" was blocked.");
    }
  }
  public static int random_range(int low, int high)
  {
    int size = high - low + 1;
    return (int)(Math.random() * size) + low;
  }
  public static Warrior battle(Warrior thisGuy, Warrior thatGuy)
  {
    /*
     * Write the code that makes these 2 warriors fight.
     * Each of them "swings" and "defends" at the same time
     *  --> p1 attacks p2
     *  --> p2 attacks p1
     * As long as neither's hp is empty, keep fighting
     * return either the player who has HP's left, or null if they KO'd each other.
     */
    while(thisGuy.hp > 0 && thatGuy.hp > 0)
    {
      thisGuy.attack(thatGuy);
      thatGuy.attack(thisGuy);
      System.out.println(thisGuy);
      System.out.println(thatGuy);
    }
    if(thisGuy.hp <= 0 && thatGuy.hp <= 0)
    {
      System.out.println("Both warriors have fallen!");
      return null;
    }
    else if(thisGuy.hp <= 0)
    {
      System.out.println(thatGuy.name + " has won the battle!");
      return thatGuy;
    }
    else
    {
      System.out.println(thisGuy.name + " has won the battle!");
      return thisGuy;
    }
  }

  //Testing main method
  public static void main(String[] args) 
  {
    Warrior p1 = new Warrior("Bart", 18, 13, 90);
    Warrior p2 = new Warrior();
    System.out.println(p1);
    System.out.println(p2);
    p1.attack(p2);
    System.out.println(p1);
    System.out.println(p2);
    battle(p1, p2);
  }
}
