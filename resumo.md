

# Do Java programmers write better Python? Studying Off-Language Code Quality on Github
* Este trabalho analisa códigos Python feitos por pessoas que tem mais prática com Java ou C++
* A principal conclusão do trabalho é de que "boas práticas mais gerais foram normalmente aplicadas" por estes desenvolvedores "off-language", todavia as boas práticas python-específicas são usualmente violadas.
* Esta conclusão é um argumento que demonstra a importância de estudos voltados apenas para as boas práticas Python-específicas

# The Prevalence of Code Smells in Machine Learning projects

O trabalho [3] é muito semelhante ao nosso! Podemos apresentar o nosso como sendo uma expansão deste!

Algo a ser considerado aqui é que eles também utilizam Pylint e também detectam os mesmos "pitfalls" que detectamos, **porém eles chamam apenas de "code smells", assim como [1] chama de "bugs não funcionais" e [4] generaliza como "defects".**

O trabalho foi feito da seguinte forma:
- Pegaram 74 soluções de problemas do Kaggle (nós pegamos mais de mil repositórios do Github)
- Com o código destas 74 soluções, eles executaram o Pylint **com a configuração padrão** e coletaram as top 20 mensagens dadas pela ferramenta em cada uma das quatro categorias (Convention, Error, Refactor, Warning
- Descreveram os resultados e só. Não desenvolveram maiores aprofundamentos, apenas indicaram os smells mais recorrentes.

Principais diferenças entre os nossos trabalhos:
* Coletamos bem mais fontes de código, mais de mil repositórios contra 74 respostas de problemas do Kaggle.
* Ganhamos em "generalização" de público, porém eles focaram em "códigos de soluções de machine learning", ou seja: algoritmos para resolver problemas de ML e não soluções, frameworks e sistemas gerais.
* Eles utilizaram o Pylint indiscriminadamente e isto usualmente não é bom, pois o detector pega muitos falsos positivos. Inclusive tivemos problemas com isso no caso do pitfall "atributo definido fora do construtor", onde o Pylint detecta todas [dataclasses](https://docs.python.org/3/library/dataclasses.html) como sendo um caso e por isto este pitfall foi delistado.

**Ambos os trabalhos detectaram:**
- singleton-comparison
- consider-using-enumerate
- consider-using-in
- dangerous-default-value
- redefined-built-in

**Apenas o nosso trabalho detectou**
- consider-using-with


Ou seja: Ele cita praticamente todos os nossos "pitfalls" e alguns outros. Uma missão que teríamos seria explicar o motivo de termos escolhido apenas este pequeno subset para o nosso trabalho. Alguns argumentos em defesa da escolha podem ser montados utilizando a conclusão de [5]. Ou também que seria muito complicado falar sobre 80 pitfalls na survey e ninguém ficaria respondendo 80 questões.

# A dataset of non-functional bugs

Em [1] o objetivo foi montar um dataset [2] de "bugs não funcionais". O paper define bugs não funcionais como "bugs que prejudicam os requisitos não funcionais da aplicação", como por exemplo: construções de código que deixam a aplicaçao lenta.
Dentro do dataset alguns casos do que chamamos de pitfalls foram classificados como bug não funcional.
Como por exemplo, [essa entrada do dataset](https://github.com/ualberta-smr/NFBugs/tree/master/py-data/VS_test) classifica uma entrada de **C0200 consider-using-enumerate** como bug não funcional e nessa classificam [manual ~~file~~ resource handler](https://github.com/ualberta-smr/NFBugs/blob/master/py-data/peewee/problems/api-related/1/problem.yml)
Todavia o paper analisou apenas 65 repositórios e nem todos eles foram de Python, alguns foram de Java e as análises não foram feitas no código ao todo do projeto, mas sim apenas nas modificações que alguns commits subiram para o repositório. Esta análise foi puramente manual.
A principal contribuição deste paper para nós seria "colocar em pauta" alguns dos pitfalls que comentamos.

# Study of Defects in a Program Code in Python
* Defende que os erros encontrados em Python são diferentes dos encontrados em outras linguagens, logo Python deve ser estudado de forma "separada". (argumento para justificar a importância do nosso trabalho)
* Cita que em cenários onde a refatoração indicada para o caso de 'consider-using-in' seja utilizada "é impossível que ocorra erros de violação de limites de arrays"

# Do developers care about code smells? An exploratory survey
* É um paper de 2013
* Conduziram uma survey parecida com a nossa
* Obtiveram 73 respostas (85 responderam, mas só 73 foram até o fim)
* Em resumo os resultados foram bem negativos, com a maioria dizendo não saber ou não aplicar soluções de qualidade de código, de toda forma é uma survey antiga
* Apenas 18% dos respondentes afirmaram saber o que são code smells
* **TODO:** Este paper é bem citado, conferir se a survey foi refeita mais recentemente.

# An exploration of technical debt
* Definição de débito técnico
* É um paper de 2012
* Estimativa de 500 bilhões de dólares de débito técnico acumulado

# Software Aging
* Palestra do David Parnas sobre envelhecimento de software
* Associado com entropia de software







[1] [A dataset of non-functional bugs](https://sci-hub.st/https://ieeexplore.ieee.org/abstract/document/8816810/)

[2] [Non-functional bugs (Github)](https://github.com/ualberta-smr/NFBugs)

[3] [The Prevalence of Code Smells in Machine Learning projects
](https://arxiv.org/abs/2103.04146)

[4] [Study of Defects in a Program Code in Python](https://sci-hub.st/https://link.springer.com/article/10.1134/S0361768813060017)

[5] [Do Java programmers write better Python? Studying Off-Language Code Quality on Github](https://sci-hub.st/https://dl.acm.org/doi/abs/10.1145/3191697.3214341)

[6] [Do developers care about code smells? An exploratory survey](https://ieeexplore.ieee.org/abstract/document/6671299)

[7] [An exploration of technical debt](https://sci-hub.st/https://www.sciencedirect.com/science/article/abs/pii/S0164121213000022)

[8] [Software Aging](https://www.cs.drexel.edu/~bmitchel/course/cs575/SoftwareAging.pdf)

[9] [How changes affect software entropy: an empirical study](https://www.researchgate.net/profile/Marta-Cimitile/publication/241253005_How_changes_affect_software_entropy_An_empirical_study/links/00b7d5227551ea355d000000/How-changes-affect-software-entropy-An-empirical-study.pdf)

[10] [A Study of C/C++ Code Weaknesses on Stack Overflow](www.google.com)

# Dicas do Rohit
* Trabalhar nas implicações: São pessoas de fora de Python estão cometendo estes pitfalls?
    * Os cursos de Python estão indicando construções de código com qualidade?
    * Indicar soluções para pessoas que estão cometendo os smells (Curso? usar Pylint?)

# Dicas Rodrigo
* Por que as pessoas escrevem códigos ruins em Python? Será que é porque o Stack Overflow apresenta exemplos ruins? seria um trabalho futuro.
* "Quem está incentivando as issues? Stack Overflow? Livros? Tutoriais?"

# Dicas Márcio
* "Explicar bem o porquê de as issues serem ruins. Uma possível justificativa poderia ser tirada do próprio Pylint"
* "Explicar os motivos das rejeições dos PR."




