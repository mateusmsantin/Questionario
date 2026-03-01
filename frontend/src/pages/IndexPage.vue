<template>
  <q-page class="flex flex-center column q-pa-lg">

    <q-card style="max-width: 700px; width: 100%">

      <q-card-section>
        <div class="text-h6">
          Termo de Consentimento para Participação em Pesquisa
        </div>
      </q-card-section>

      <q-card-section class="text-body2 scroll" style="max-height: 400px">

        <p><strong>Pesquisa realizada por:</strong> [Associação Lagoa Mirim], CNPJ [58.452.315/0001-50], e-mail para contato: [alm.lagoa.mirim@gmail.com]</p>

        <p>
          Você está sendo convidado(a) a participar de uma pesquisa online.
          A participação é voluntária e você pode interromper a qualquer momento.
        </p>

        <p><strong>1. Quais dados serão coletados</strong></p>
        <p>Serão coletadas as seguintes informações:</p>
        <ul>
          <li>Nome completo</li>
          <li>E-mail</li>
          <li>Telefone</li>
          <li>CPF</li>
          <li>Faixa etária</li>
          <li>Gênero</li>
          <li>Raça/etnia</li>
          <li>Nome da organização (se aplicável)</li>
          <li>Localidade da organização</li>
          <li>Tipo de organização</li>
          <li>Informação sobre participação anterior em projeto da associação</li>
        </ul>

        <p>
          ⚠️ Atenção: Gênero e raça/etnia são considerados dados pessoais sensíveis
          nos termos da Lei nº 13.709/2018 (LGPD).
        </p>

        <p><strong>2. Finalidade da coleta</strong></p>
        <ul>
          <li>Mapeamento do perfil dos participantes</li>
          <li>Análise estatística e institucional</li>
          <li>Avaliação de impacto de projetos</li>
          <li>Comunicação institucional relacionada à pesquisa</li>
        </ul>

        <p>
          Os resultados poderão ser divulgados de forma anonimizada,
          sem identificação individual.
        </p>

        <p><strong>3. Compartilhamento</strong></p>
        <p>
          Seus dados não serão comercializados e não serão compartilhados com terceiros, exceto:
        </p>
        <ul>
          <li>Quando houver obrigação legal;</li>
          <li>Quando necessário para execução da pesquisa (ex: plataforma de armazenamento de dados).</li>
        </ul>

        <p><strong>4. Armazenamento e segurança</strong></p>
        <p>
          Os dados serão armazenados em ambiente seguro pelo prazo de
          [5 meses], sendo posteriormente eliminados ou anonimizados.
        </p>

        <p><strong>5. Seus direitos (LGPD)</strong></p>
        <p>Você pode, a qualquer momento:</p>
        <ul>
          <li>Solicitar acesso aos seus dados</li>
          <li>Corrigir informações</li>
          <li>Solicitar exclusão (quando aplicável)</li>
          <li>Revogar este consentimento</li>
        </ul>

        <p>
          Para isso, entre em contato pelo e-mail: [alm.lagoa.mirim@gmail.com]
        </p>

      </q-card-section>

      <q-separator />

      <q-card-section>
        <q-checkbox
          v-model="aceitou"
          label="Li e concordo com os termos da pesquisa"
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          label="Participar da Pesquisa"
          color="primary"
          :disable="!aceitou"
          @click="irParaQuestionario"
        />
      </q-card-actions>

    </q-card>

  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'IndexPage',

  setup () {
    const aceitou = ref(false)
    const router = useRouter()

    function irParaQuestionario () {
      router.push('/questionario')
    }

    return {
      aceitou,
      irParaQuestionario
    }
  }
})
</script>
