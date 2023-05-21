#include <stdio.h>  
#include <stdlib.h>  
#include <stdint.h>  
#include <sys/types.h>  
#include <sys/stat.h>  
#include <fcntl.h>  
#include <string.h>  

char empty_sound[8] = { 4, 0, 0, 0, 6, 0, 6, 0 };  

struct wav_header {  
    // "RIFF" chunk descriptor  
    int32_t  chunk_id;  
    int32_t  chunk_sz;  
    int32_t  format;  
    // "fmt (header)" sub-chunk  
    int32_t  sub_chunk1_id;  
    int32_t  sub_chunk1_sz;  
    int16_t  audio_format;  
    int16_t  num_channel;  
    int32_t  sample_rate;  
    int32_t  byte_rate;  
    int16_t  block_align;  
    int16_t  bits_per_sample;  
    // "data (easily, music)" sub-chunk  
    int32_t  sub_chunk2_id;  
    int32_t  sub_chunk2_sz;  
    char   *data;  
};  

#define ONE_SEC 88200  // bytes  

static void print_header(struct wav_header *hdr)  
{  
    printf("(0) chunk id  : %x\n", hdr->chunk_id);  
    printf("(4) chunk size : %d\n", hdr->chunk_sz);  
    printf("(8) format   : %x\n\n", hdr->format);  
    printf("(12) sub chunk1 id  : %d\n", hdr->sub_chunk1_id);  
    printf("(16) sub chunk1 size : %d\n", hdr->sub_chunk1_sz);  
    printf("(20) audio format  : %d\n", hdr->audio_format);  
    printf("(22) num channels  : %d\n", hdr->num_channel);  
    printf("(24) sample rate   : %d\n", hdr->sample_rate);  
    printf("(28) byte rate    : %d\n", hdr->byte_rate);  
    printf("(32) block align   : %d\n", hdr->block_align);  
    printf("(34) bits per sample : %d\n\n", hdr->bits_per_sample);  
    printf("(36) sub chunk2 id  : %d\n", hdr->sub_chunk2_id);  
    printf("(40) sub chunk2 size : %d\n", hdr->sub_chunk2_sz);  
    printf("(44 -- ) DATA\n\n");  
}  

static int bytes_for_sec(int bpm)  
{  
    float ratio = bpm/60.0;  
    float bytes_per_beep = ONE_SEC / ratio;  
    return (int)bytes_per_beep;  
}  

int main(int argc, char **argv)  
{  
    char *sample_fname;  
    int tempo, dura, bps;  
    int rfd;       // Sample file descriptor  
    int wfd;       // Output file descriptor  
    int rc, i, j, tot_beats;  
    char buf[512 + 1];   // Sample hdr buffer  
    char *sample_buf, *ptr;  
    struct wav_header *hdr;  
    struct wav_header new_hdr;  
    if (argc < 3) {  
	printf("USAGE: %s <sample_wav> <tempo in BPM> <duration in sec>\n", argv[0] );  
	printf(" * sample_wav must be aligned by sample. Random clip of data may make a noise.\n");  
	printf(" example: $ %s s3.wav 120 60\n", argv[0]);  
	printf("  This will make an output of 'a.wav', using s3.wav as sample, 120 bps for 60sec.\n");  
	exit(0);  
    }  
    sample_fname = argv[1];  
    tempo = atoi(argv[2]);  
    if (tempo < 40) {  
	printf("Invalid tempo:  Make it between 40 - MAX, which is the fastest from sample\n");  
	exit(1);  
    }  
    dura = atoi(argv[3]);  
    if (dura == 0) {  
	printf("Invalid duration: Make it greater than 0.\n");  
	exit(2);  
    }  
    rfd = open(sample_fname, O_RDONLY);  
    rc = read(rfd, buf, 44);  
    if (rc < 0) {  
	perror("Sample read error\n");  
	exit(3);  
    }  
    hdr = (struct wav_header *)buf;  
    if ( NULL == (sample_buf = malloc( hdr->sub_chunk2_sz )) ) {  
	perror("Mem alloc failed (1)\n");  
	exit(4);  
    }  
    // copying sample data  
    ptr = sample_buf;  
    while ( 0 < (rc = read(rfd, ptr, 512)) ) {  
	ptr += rc;  
    }  
    wfd = open("t.wav" , O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);  
    if (wfd < 0) {  
	perror("Error opening write file");  
    }  
    tot_beats = dura * (tempo/60.0);  
    bps = bytes_for_sec(tempo);  
    int tot_bytes = 0;  
    for (i =0; i<tot_beats; ++i) {  
	write(wfd, sample_buf, hdr->sub_chunk2_sz);  
	tot_bytes += hdr->sub_chunk2_sz;  
	for (j = 0; j< (bps - hdr->sub_chunk2_sz)/8; ++j) {  
	    write(wfd, empty_sound, 8);  
	    tot_bytes += 8;  
	}  
    }  
    close(wfd);  
    memcpy(&new_hdr, hdr, 44);  
    new_hdr.sub_chunk2_sz=tot_bytes;  
    wfd = open("h.wav", O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);  
    write(wfd, &new_hdr, 44);  
    close(wfd);  
    system("/bin/cat h.wav t.wav > a.wav");  
    return 0;  
}  
