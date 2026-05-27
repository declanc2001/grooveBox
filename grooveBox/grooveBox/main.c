#include <alsa/asoundlib.h>
#include <stdint.h>
#include <stdio.h>

extern int32_t next_sample(uint32_t *phase, uint32_t increment);

int main(void)
{
    snd_pcm_t *pcm;
    snd_pcm_hw_params_t *params;

    unsigned int rate = 44100;
    int dir = 0;

    snd_pcm_uframes_t period_size = 256;
    snd_pcm_uframes_t buffer_size = 1024;

    int rc = snd_pcm_open(&pcm, "default", SND_PCM_STREAM_PLAYBACK, 0);
    if (rc < 0) {
        fprintf(stderr, "unable to open PCM device: %s\n", snd_strerror(rc));
        return 1;
    }

    snd_pcm_hw_params_alloca(&params);
    snd_pcm_hw_params_any(pcm, params);

    snd_pcm_hw_params_set_access(pcm, params, SND_PCM_ACCESS_RW_INTERLEAVED);
    snd_pcm_hw_params_set_format(pcm, params, SND_PCM_FORMAT_S16_LE);
    snd_pcm_hw_params_set_channels(pcm, params, 1);
    snd_pcm_hw_params_set_rate_near(pcm, params, &rate, &dir);

    snd_pcm_hw_params_set_period_size_near(pcm, params, &period_size, &dir);
    snd_pcm_hw_params_set_buffer_size_near(pcm, params, &buffer_size);

    rc = snd_pcm_hw_params(pcm, params);
    if (rc < 0) {
        fprintf(stderr, "unable to set hw params: %s\n", snd_strerror(rc));
        snd_pcm_close(pcm);
        return 1;
    }

    int16_t buffer[256];
    uint32_t phase = 0;
    float freq = 220.0f;
    uint32_t increment = 0;
    float env = 0.0f;
    int previous_gate = 0;
    float filtered = 0.0f;

    increment = (uint32_t)(((uint64_t)((uint32_t)freq) << 32) / rate);

    int last_gate = -1;

    printf("oscillator_audio running...\n");

    while (1)
{
    int gate = 0;
    int slide = 0;

    uint32_t amp = 1024;
    uint32_t decay_value = 9950;
    uint32_t cutoff_value = 500;

    FILE *cutoff_file = fopen("/home/declanc01/grooveBox/cutoff.txt", "r");
    if (cutoff_file != NULL) {
       fscanf(cutoff_file, "%u", &cutoff_value);
       fclose(cutoff_file);
    }

    float cutoff = cutoff_value / 1000.0f;

    FILE *slide_file = fopen("/home/declanc01/grooveBox/slide.txt", "r");
    if (slide_file != NULL) {
       fscanf(slide_file, "%d", &slide);
       fclose(slide_file);
}

    FILE *amp_file = fopen("/home/declanc01/grooveBox/amp.txt", "r");
    if (amp_file != NULL) {
       fscanf(amp_file, "%u", &amp);
       fclose(amp_file);
}
    FILE *decay_file = fopen("/home/declanc01/grooveBox/decay.txt", "r");
    if (decay_file != NULL) {
       fscanf(decay_file, "%u", &decay_value);
       fclose(decay_file);
}

float decay = decay_value / 10000.0f;



    FILE *f = fopen("/home/declanc01/grooveBox/gate.txt", "r");
    if (f != NULL) {
        fscanf(f, "%d", &gate);
        fclose(f);
    }

    FILE *freq_file = fopen("/home/declanc01/grooveBox/freq.txt", "r");

    if (freq_file != NULL) {

        unsigned int new_freq;

        if (fscanf(freq_file, "%u", &new_freq) == 1) {

            if (slide == 1) {
                freq = freq + ((new_freq - freq) * 0.02);  
            } else {  
                freq = new_freq;
            }
    

            increment = (uint32_t)(((uint64_t)freq << 32) / rate);
        }

        fclose(freq_file);
    }

    if (gate != last_gate) {
            printf("gate changed to %d\n", gate);
            fflush(stdout);
            last_gate = gate;
        }

        for (int i = 0; i < 256; i++)
        {
            if (gate == 1) {
                if (gate == 1 && previous_gate == 0) {
                    env = 1.0f;   
                }

                int32_t sample = next_sample(&phase, increment);

                filtered = filtered + cutoff * ((float)sample - filtered);

                sample = (int32_t)(filtered * env);

                buffer[i] = sample;

                env *= decay;    




            } else {
                buffer[i] = 0;
            }
        }

        previous_gate = gate;
        rc = snd_pcm_writei(pcm, buffer, 256);

        if (rc == -EPIPE) {
            snd_pcm_prepare(pcm);
        } else if (rc < 0) {
            fprintf(stderr, "write failed: %s\n", snd_strerror(rc));
            break;
        }
    }

    snd_pcm_drain(pcm);
    snd_pcm_close(pcm);
    return 0;
}