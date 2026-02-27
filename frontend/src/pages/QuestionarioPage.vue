<template>
  <q-page class="q-pa-md">
    <div class="row justify-end q-mb-md">
      <q-btn v-if="user" flat color="negative" label="Sair" icon="logout" @click="logout" />
    </div>

    <div v-if="!user">
      <q-card class="q-pa-md shadow-2" style="max-width: 400px; margin: auto">
        <div class="text-h6 q-mb-md text-center">
          {{ modoRegistro ? 'Crie sua Conta' : 'Acesso ao Sistema' }}
        </div>

        <div class="row justify-center q-mb-md">
          <q-btn-toggle
            v-model="modoRegistro"
            toggle-color="primary"
            flat
            :options="[
              { label: 'Fazer o cadastro', value: true },
              { label: 'Responder Questionário', value: false }

            ]"
          />
        </div>

        <q-input v-model="email" label="E-mail" outlined dense class="q-mt-md"

          type="email"
          :rules="[
            val => !!val || 'E-mail é obrigatório',
            val => /.+@.+\..+/.test(val) || 'Digite um e-mail válido'
          ]"
          lazy-rules
        />
        <q-input
          v-model="password"
          label="Senha"
          type="password"
          outlined
          dense
          class="q-mt-md"
        />

        <q-slide-transition>
          <div v-if="modoRegistro">
            <q-input
              v-model="confirmPassword"
              label="Confirme sua Senha"
              type="password"
              outlined
              dense
              class="q-mt-md"
              :error="confirmPassword !== '' && password !== confirmPassword"
              error-message="As senhas não conferem"
            />
          </div>
        </q-slide-transition>

        <q-btn
          :label="modoRegistro ? 'Registrar e Iniciar' : 'Entrar'"
          color="primary"
          class="q-mt-md full-width"
          @click="validarAcaoLogin"
          :disabled="modoRegistro && (password !== confirmPassword || !password)"
        />
      </q-card>
    </div>
    <div v-else-if="jaRespondeu" class="column items-center q-pa-xl text-center">
      <q-icon name="task_alt" color="positive" size="80px" />
      <div class="text-h5 q-mt-md">Formulário já preenchido!</div>
      <p class="text-subtitle1 text-grey-8">Seu e-mail ({{ email }}) já enviou as respostas.</p>
      <q-btn label="Sair" color="primary" outline class="q-mt-lg" @click="logout" />
    </div>

    <div v-else-if="!profile">
      <q-card flat bordered class="q-pa-md shadow-2">
        <q-card-section class="text-center">
          <div class="text-h6 text-primary">Cadastro de Perfil</div>
          <p class="text-caption">Preencha seus dados para liberar o questionário.</p>
        </q-card-section>

        <q-form @submit.prevent="salvarProfile" class="q-pa-md">
          <div class="row q-col-gutter-sm">
            <q-input class="col-12" v-model="profileData.nome_completo" label="1. Nome completo" outlined dense
              :error="!!errosServidor.nome_completo" :error-message="errosServidor.nome_completo?.[0]" />

            <q-input class="col-sm-6 col-12" v-model="profileData.email_contato" label="2. E-mail de contato" outlined dense readonly bg-color="grey-2" />

            <q-input class="col-sm-6 col-12" v-model="profileData.telefone" label="3. Telefone" mask="(##) #####-####" outlined dense
              :error="!!errosServidor.telefone" :error-message="errosServidor.telefone?.[0]" />

            <q-input class="col-12" v-model="profileData.cpf" label="4. CPF" mask="###.###.###-##" unmasked-value outlined dense
              :error="!!errosServidor.cpf" :error-message="errosServidor.cpf?.[0]" />

            <q-select class="col-sm-6 col-12" v-model="profileData.faixa_etaria" label="5. Faixa etária" :options="ageOptions" emit-value map-options outlined dense
              :error="!!errosServidor.faixa_etaria" :error-message="errosServidor.faixa_etaria?.[0]" />

            <q-select class="col-sm-6 col-12" v-model="profileData.genero" label="6. Gênero" :options="genderOptions" emit-value map-options outlined dense
              :error="!!errosServidor.genero" :error-message="errosServidor.genero?.[0]" />

            <q-select class="col-12" v-model="profileData.raca" label="7. Identidade étnico-racial" :options="raceOptions" emit-value map-options outlined dense
              :error="!!errosServidor.raca" :error-message="errosServidor.raca?.[0]" />

            <q-input class="col-12" v-model="profileData.nome_organizacao" label="8. Organização" outlined dense
              :error="!!errosServidor.nome_organizacao" :error-message="errosServidor.nome_organizacao?.[0]" />

            <q-input class="col-sm-7 col-12" v-model="profileData.localidade_organizacao" label="9. Localidade" outlined dense
              :error="!!errosServidor.localidade_organizacao" :error-message="errosServidor.localidade_organizacao?.[0]" />

            <q-select class="col-sm-5 col-12" v-model="profileData.tipo_organizacao" label="10. Tipo" :options="orgTypeOptions" emit-value map-options outlined dense
              :error="!!errosServidor.tipo_organizacao" :error-message="errosServidor.tipo_organizacao?.[0]" />

            <q-toggle v-model="profileData.participou_projeto" label="11. Já participou do Projeto Lagoa Mirim?" class="col-12" />
          </div>

          <q-btn type="submit" label="Salvar e Continuar" color="positive" class="full-width q-mt-md" size="lg" />
        </q-form>
      </q-card>
    </div>

    <div v-else-if="abas && abas.length > 0">
      <q-tabs v-model="tabIndex" dense active-color="primary" indicator-color="primary" align="justify" class="bg-white shadow-1">
        <q-tab v-for="(aba, index) in abas" :key="aba.id" :name="index" :label="aba.nome" :disabled="index > 0 && !abaCompleta(index - 1)" />
      </q-tabs>

      <q-separator />

      <q-tab-panels v-model="tabIndex" animated class="q-mt-md">
        <q-tab-panel v-for="(aba, index) in abas" :key="aba.id" :name="index" class="q-pa-none">
          <div v-for="pergunta in aba.perguntas" :key="pergunta.id" class="q-mb-lg q-pa-md bg-white border-radius-inherit shadow-1">
            <div class="text-subtitle1 q-mb-md"><strong>{{ pergunta.texto }}</strong></div>
            <div class="row justify-center">
              <q-btn-toggle v-model="respostas[pergunta.id]" spread no-caps toggle-color="primary" color="grey-3" text-color="black"
                :options="[{label:'1',value:1},{label:'2',value:2},{label:'3',value:3},{label:'4',value:4},{label:'5',value:5}]"
                @update:model-value="verificarProgresso(index)" />
            </div>
          </div>

          <div class="row justify-between q-pa-md">
            <q-btn flat label="Anterior" @click="tabIndex--" :disabled="tabIndex === 0" />
            <q-btn v-if="index < abas.length - 1" color="primary" label="Próxima" :disabled="!abaCompleta(index)" @click="tabIndex++" />
            <q-btn v-else color="positive" label="Finalizar e Enviar" icon="send" :disabled="!questionarioTodoCompleto()" @click="enviarRespostas" />
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
<div v-else class="text-center q-pa-xl">
      <div v-if="user && profile && abas.length === 0">
        <q-icon name="error_outline" color="warning" size="50px" />
        <p class="q-mt-md">Você está logado, mas não encontramos perguntas cadastradas.</p>
        <q-btn flat label="Tentar novamente" color="primary" @click="carregarAbas" />
      </div>
      <div v-else>
        <q-spinner-dots color="primary" size="40px" />
        <p class="text-grey">Sincronizando dados para {{ user }}...</p>
      </div>
    </div>

  </q-page>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const user = ref(null)
const profile = ref(null)
const jaRespondeu = ref(false)
const email = ref('')
const password = ref('')
const abas = ref([])
const respostas = ref({})
const tabIndex = ref(0)
const abaMaxLiberada = ref(0)
const errosServidor = ref({})

const profileData = reactive({
  nome_completo: '', email_contato: '', telefone: '', cpf: '',
  faixa_etaria: '', genero: '', raca: '', nome_organizacao: '',
  localidade_organizacao: '', tipo_organizacao: '', participou_projeto: false
})

const ageOptions = [
  { label: 'Até 18', value: 'A18' }, { label: '19 a 30', value: '19_30' },
  { label: '31 a 40', value: '31_40' }, { label: '41 a 50', value: '41_50' },
  { label: '51 a 60', value: '51_60' }, { label: '60+', value: '60+' }
]
const genderOptions = [
  { label: 'Mulher cis', value: 'MC' }, { label: 'Homem cis', value: 'HC' },
  { label: 'Trans', value: 'TR' }, { label: 'Não binário', value: 'NB' }, { label: 'Outro', value: 'OUT' },
  { label: 'Mulher Trans', value: 'MT' }, { label: 'Homem HT', value: 'HT' }



]
const raceOptions = [
  { label: 'Indígena', value: 'IND' }, { label: 'Preto(a)', value: 'AFR' },
  { label: 'Branca', value: 'BRA' }, { label: 'Parda', value: 'PAR' }, { label: 'Asiática', value: 'ASI' }
]
const orgTypeOptions = [
  { label: 'ONG/Coletivo', value: 'SOC' }, { label: 'Indivíduo', value: 'IND' },
  { label: 'Governo', value: 'GOV' }, { label: 'Educação', value: 'EDU' }, { label: 'Privado', value: 'PRI' }
]

const loginUser = async () => {
  try {
    // LIMPEZA: Remove qualquer token antigo antes de tentar um novo login
    localStorage.removeItem('access_token')
    delete api.defaults.headers.common['Authorization']

    const res = await api.post('/login-or-register/', {
      email: email.value,
      password: password.value
    })

    // Se o Django retornou sucesso, aí sim guardamos o novo
    const token = res.data.access
    localStorage.setItem('access_token', token)
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`

    user.value = email.value
    profileData.email_contato = email.value

    await carregarProfile()
  } catch (err) {
    const msg = err.response?.data?.detail || 'Erro ao entrar. Verifique e-mail e senha.'
    $q.notify({ color: 'negative', message: msg })
  }
}


const carregarProfile = async () => {
  try {
    const res = await api.get('/profile/')
    const dados = Array.isArray(res.data) ? res.data[0] : res.data

    if (dados && dados.id) {
      profile.value = dados

      // Tentamos carregar as abas, mas envolvemos em um try/catch interno
      // para que um erro nas abas não trave a lógica do perfil
      try {
        await carregarAbas()
      } catch (abaErr) {
        console.error("Perfil OK, mas erro ao carregar abas:", abaErr)
      }
    } else {
      profile.value = null
      profileData.email_contato = user.value
    }
  } catch (err) {
    profile.value = null
    profileData.email_contato = user.value
  }
}

const carregarAbas = async () => {
  try {
    const res = await api.get('/abas/')

    // Verificação de "Já respondeu"
    if (res.data.ja_respondido === true) {
      jaRespondeu.value = true
      return
    }

    const lista = Array.isArray(res.data) ? res.data : (res.data.results || [])

    if (lista.length > 0) {
      abas.value = lista
    } else {
      // Se não houver abas, avisamos para não ficar no "Sincronizando" eterno
      $q.notify({ color: 'warning', message: 'Nenhum questionário ativo encontrado.' })
      // Opcional: abaMaxLiberada.value = -1 ou algo que tire do spinner
    }
  } catch (err) {
    console.error("Erro ao carregar abas", err)
    $q.notify({ color: 'negative', message: 'Erro ao carregar perguntas.' })
  }
}
const salvarProfile = async () => {
  errosServidor.value = {}
  console.log("Tentando salvar perfil...");

  try {
    const res = await api.post('/profile/', profileData)

    console.log("Resposta do servidor:", res.status);

    // Se criou com sucesso (201) ou já existia (200)
    if (res.status === 201 || res.status === 200) {
      // Usamos alert nativo para garantir que NADA bloqueie o aviso
      alert('✅ Perfil Salvo com Sucesso!\n\nClique em OK para fazer login novamente e responder ao questionário.');

      // Chamamos o logout IMEDIATAMENTE após o OK do alert
      logout();
    }
  } catch (err) {
    console.error("Erro capturado no catch:", err.response?.status, err.response?.data);

    if (err.response?.status === 400) {
      const msgErro = JSON.stringify(err.response.data);

      // Se o erro for de duplicidade (o 400 que você viu no log)
      if (msgErro.includes('já existe') || msgErro.includes('unique')) {
        alert('Este perfil já está cadastrado. Vamos redirecionar você para o login.');
        logout();
      } else {
        errosServidor.value = err.response.data;
        $q.notify({ color: 'negative', message: 'Verifique os campos obrigatórios.' });
      }
    } else {
      $q.notify({ color: 'negative', message: 'Erro de conexão com o servidor.' });
    }
  }
}

const abaCompleta = (idx) => {
  const aba = abas.value[idx]
  if (!aba || !aba.perguntas) return false

  // Verifica se TODAS as perguntas daquela aba possuem uma resposta no objeto
  return aba.perguntas.every(pergunta => {
    const valor = respostas.value[pergunta.id]
    return valor !== undefined && valor !== null
  })
}

const verificarProgresso = (idx) => {
  if (abaCompleta(idx)) {
    // Se a aba atual está completa, liberamos a próxima
    if (abaMaxLiberada.value === idx) {
      abaMaxLiberada.value = idx + 1
    }
  }
}

const enviarRespostas = async () => {
  try {
    const payload = Object.keys(respostas.value).map(id => ({ pergunta: parseInt(id), peso: respostas.value[id] }))
    await api.post('/submit-respostas/', payload)
    jaRespondeu.value = true
    $q.notify({ color: 'positive', message: 'Respostas enviadas!' })
  } catch { $q.notify({ color: 'negative', message: 'Erro ao enviar respostas.' }) }
}

const logout = () => {
  // 1. Limpa o Token
  localStorage.removeItem('access_token')
  delete api.defaults.headers.common['Authorization']

  // 2. Reseta os estados de controle
  user.value = null
  profile.value = null
  jaRespondeu.value = false
  abas.value = []
  respostas.value = {}
  tabIndex.value = 0
  abaMaxLiberada.value = 0

  // 3. ZERA O FORMULÁRIO (Isso resolve o e-mail travado)
  Object.assign(profileData, {
    nome_completo: '',
    email_contato: '',
    telefone: '',
    cpf: '',
    faixa_etaria: '',
    genero: '',
    raca: '',
    nome_organizacao: '',
    localidade_organizacao: '',
    tipo_organizacao: '',
    participou_projeto: false
  })

  // 4. Limpa as credenciais de login
  email.value = ''
  password.value = ''
  confirmPassword.value = ''
  errosServidor.value = {}

  $q.notify({ message: 'Sessão encerrada', color: 'info', icon: 'logout' })
}

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    // Só tenta carregar se o token for válido
    carregarProfile().catch(() => logout())
  }
})


const modoRegistro = ref(false) // Controla se mostra o campo de confirmar senha
const confirmPassword = ref('') // Armazena a segunda senha

const validarAcaoLogin = () => {
  // Regex simples para validar formato de e-mail
  const emailPattern = /.+@.+\..+/;

  if (!email.value || !emailPattern.test(email.value)) {
    $q.notify({ color: 'negative', message: 'Por favor, insira um e-mail válido.' })
    return
  }

  if (modoRegistro.value) {
    if (password.value !== confirmPassword.value) {
      $q.notify({ color: 'negative', message: 'As senhas precisam ser iguais!' })
      return
    }
    if (password.value.length < 6) {
      $q.notify({ color: 'negative', message: 'A senha deve ter pelo menos 6 caracteres.' })
      return
    }
  }

  // Se passou em tudo, chama o login/registro
  loginUser()
}


const questionarioTodoCompleto = () => {
  // Percorre todas as abas e verifica se cada uma está completa
  return abas.value.every((aba, index) => abaCompleta(index))
}

</script>
